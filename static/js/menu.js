/* Cuando hago Clic .button, nav Toggle `activo` */
const button = document.querySelector('.button')
const nav    = document.querySelector('.navbar')

button.addEventListener('click',()=>{
    nav.classList.toggle('activo')
})
