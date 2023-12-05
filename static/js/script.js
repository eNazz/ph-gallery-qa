const fulImgBox = document.getElementById("fulImgBox");
const fulImg = document.getElementById("fulImg");

function openFulImg(reference) {
    fulImgBox.style.display = "flex";
    fulImg.src = reference;
}

function closeImg() {
    fulImgBox.style.display = "none";
}

const nombreInput = document.getElementById('nombre');
const comentarioInput = document.getElementById('comentario');
const comentarioLista = document.getElementById('comentario-lista');
window.onload = function () {
    const agregarComentarioBtn = document.getElementById('agregar-comentario');

    if (agregarComentarioBtn) {
        agregarComentarioBtn.addEventListener('click', () => {
            const nombre = nombreInput.value;
            const comentario = comentarioInput.value;

            if (nombre && comentario) {
                agregarComentario(nombre, comentario);
                nombreInput.value = '';
                comentarioInput.value = '';
            } else {
                alert('Por favor, completa ambos campos.');
            }
        });
    }


    function agregarComentario(nombre, comentario) {
        const comentarioDiv = document.createElement('div');
        comentarioDiv.classList.add('comentario');

        const nombreParrafo = document.createElement('p');
        nombreParrafo.textContent = nombre;
        comentarioDiv.appendChild(nombreParrafo);

        const comentarioParrafo = document.createElement('p');
        comentarioParrafo.textContent = comentario;
        comentarioDiv.appendChild(comentarioParrafo);

        comentarioLista.appendChild(comentarioDiv); // Agrega el comentario al DOM
    }
}
