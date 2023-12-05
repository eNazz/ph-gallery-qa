const form = document.querySelector("#form-contacto");

// Validación del nombre
const nombre = document.querySelector("#nombre");
nombre.addEventListener("blur", function() {
    if (nombre.value === "") {
        nombre.classList.add("error");
    } else {
        nombre.classList.remove("error");
    }
});

// Validación del correo electrónico
const correo = document.querySelector("#correo");
correo.addEventListener("blur", function() {
    if (correo.value === "") {
        correo.classList.add("error");
    } else if (!correo.value.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/)) {
        correo.classList.add("error");
    } else {
        correo.classList.remove("error");
    }
});

// Validación del celular
const celular = document.querySelector("#celular");
celular.addEventListener("blur", function() {
    if (celular.value === "") {
        celular.classList.add("error");
    } else if (celular.value.length < 10) {
        celular.classList.add("error");
    } else {
        celular.classList.remove("error");
    }
});

// Validación del mensaje
const mensaje = document.querySelector("#mensaje");
mensaje.addEventListener("blur", function() {
    if (mensaje.value === "") {
        mensaje.classList.add("error");
    } else {
        mensaje.classList.remove("error");
    }
});

// Validación general del formulario
form.addEventListener("submit", function(e) {
    // Si hay algún campo con error, se cancela el envío del formulario
    if (nombre.classList.contains("error") ||
        correo.classList.contains("error") ||
        celular.classList.contains("error") ||
        mensaje.classList.contains("error")) {
        // Se muestra un mensaje de error
        alert("Por favor, complete todos los campos correctamente.");
        // Se cancela el envío del formulario
        e.preventDefault();
    }
});