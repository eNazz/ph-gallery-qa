document.addEventListener("DOMContentLoaded", function () {
    // Reemplaza con tu clave de API de Pexels
    const apiKey = 'pHwZhybwpxaoSLtxL0q3IJVhyQKk7f6yLPKcn4LG2nDimbf0K4gHZtl5';
    const endpoint = `https://api.pexels.com/v1/curated?per_page=1`;

    fetch(endpoint, {
        headers: {
            'Authorization': apiKey,
        }
    })
    .then(response => response.json())
    .then(data => {
        const imageUrl = data.photos[0].src.large;
        const imageElement = document.getElementById('pexels-image');
        imageElement.src = imageUrl;
    })
    .catch(error => {
        console.error('Error al cargar la imagen desde Pexels:', error);
    });
});
