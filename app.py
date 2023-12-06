from flask import Flask, render_template, request, flash, redirect
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

app = Flask(__name__)

app.config['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
app.config['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
app.config['AWS_REGION'] = AWS_REGION

titulo = "PH Gallery"
import psycopg2


# Configurar la conexión
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

class Contacto_c:
    def __init__(self, host, port, database, user, password):
        self.conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
        )
        self.cursor = self.conn.cursor()

    def guardar_mensaje(self, nombre, correo, celular, mensaje):
        sql = f"INSERT INTO public.contacto(nombre, correo, celular, mensaje) VALUES (%s, %s, %s, %s);"
        valores = [nombre, correo, celular, mensaje]
        resp = self.cursor.execute(sql, valores)
        self.conn.commit()
        return resp

    def actualizar_mensaje(self, nombre, correo, celular, mensaje, contacto_id):
        sql = f"UPDATE public.contacto SET nombre = %s, correo = %s, celular = %s, mensaje = %s WHERE contacto_id = %s"
        valores = [nombre, correo, celular, mensaje, contacto_id]
        return self.cursor.execute(sql, valores)

    def listar_mensajes(self):
        sql = "SELECT * FROM public.contacto ORDER BY contacto_id ASC"
        self.cursor.execute(sql)
        filas = self.cursor.fetchall()
        contactos = []
        for fila in filas:
            contacto = {}
            for i, columna in enumerate(self.cursor.description):
                contacto[columna[0]] = fila[i]
            contactos.append(contacto)
        return contactos

    def eliminar_mensaje(self, contacto_id):
        sql = f"DELETE FROM public.contacto WHERE contacto_id = %s"
        valores = [contacto_id]
        self.cursor.execute(sql, valores)
        self.conn.commit()

    def buscar(self, contacto_id):
        sql = "SELECT * FROM public.contacto WHERE contacto_id = %s"
        valores = [contacto_id]
        self.cursor.execute(sql, valores)
        contacto = self.cursor.fetchone()
        if contacto is not None:
            return contacto
        else:
            return None


cont = Contacto_c(DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html', titulo=titulo)


@app.route('/contact')
def contacto_view():
    return render_template('contact.html')


@app.route('/contact', methods=['POST'])
def contacto():
    # Es uno nuevo
    if request.method == 'POST':
        nombre = request.form["nombre"]
        correo = request.form['correo']
        celular = request.form['celular']
        mensaje = request.form['mensaje']
        # Llama al el metodo para crear uno nuevo
        cont.guardar_mensaje(nombre, correo, celular, mensaje)
        mensaje_sql = "Su mensaje ha sido enviado. En breve uno de nuestros representantes se comunicara con Ud.Muchas gracias."
    return render_template('contact.html', mensaje_sql=mensaje_sql, metodo='POST')


@app.route('/listar_contact')
def listar_contact():
    contactos = cont.listar_mensajes()
    return render_template('contact_list.html', contactos=contactos)


@app.route("/eliminar/<int:contacto_id>")
def eliminar_contact(contacto_id):
    cont.eliminar_mensaje(contacto_id)
    contactos = cont.listar_mensajes()
    return render_template('contact_list.html', contactos=contactos)

@app.route("/actualizar/<int:contacto_id>")
def actualizar(contacto_id):
    contacto =  cont.buscar(contacto_id)
    contacto_id = contacto[0]
    nombre = contacto[1]
    correo= contacto[2]
    celular= contacto[3]
    mensaje= contacto[4]
    return render_template('contact_edicion.html', contacto_id=contacto_id, nombre=nombre, correo=correo,celular=celular,mensaje=mensaje)

@app.route("/actualizar_", methods=['POST'])
def actualizar_():
    # Es uno nuevo
    if request.method == 'POST':
        contacto_id = request.form["contacto_id"]
        nombre = request.form["nombre"]
        correo = request.form['correo']
        celular = request.form['celular']
        mensaje = request.form['mensaje']
        # Llama al el metodo para crear uno nuevo
        cont.actualizar_mensaje(nombre, correo, celular, mensaje, contacto_id)
        mensaje_sql = "Datos actualizados."
    contactos = cont.listar_mensajes()
    return render_template('contact_list.html', contactos=contactos)


@app.route('/galeria')
def galeria():
    return render_template('galeria.html')


@app.route('/about-us')
def aboutus():
    return render_template('about-us.html')


@app.route('/subirform')
def subirform():
    return render_template('formulario_subida.html')


@app.route('/subirimg', methods=['POST'])
def subirimg():
    # Obtener los datos del formulario
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    descripcion = request.form.get("descripcion")
    imagen = request.files["imagen"]

    # Validar los datos
    if not titulo:
        return "El título es obligatorio."
    if not autor:
        return "El autor es obligatorio."
    if not descripcion:
        return "La descripción es obligatoria."
    if not imagen:
        return "Debe seleccionar una imagen."

    # Guardar los datos en la base de datos
    import psycopg2

    conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
    )
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO imagenes (titulo, autor, descripcion, ruta)
        VALUES (%s, %s, %s, %s)
        """,
        (titulo, autor, descripcion, secure_filename(imagen.filename)),
    )
    conn.commit()
    cur.close()
    # Guardar la imagen en disco
    imagen.save(os.path.join("static/imagenes", secure_filename(imagen.filename)))
    return render_template('formulario_subida.html')


@app.route('/listar_imagen')
def listar_imagen():
    import psycopg2

    conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
    )
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
          titulo,
          autor,
          descripcion,
          ruta
        FROM
          imagenes
        ORDER BY
          titulo
        """
    )

    imagenes = []
    for row in cur:
        imagenes.append({
            "titulo": row[0],
            "autor": row[1],
            "descripcion": row[2],
            "ruta": row[3],
        })

    conn.close()
    return render_template("galeria_publica.html", imagenes=imagenes)




if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
