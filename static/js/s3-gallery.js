// Configuración de AWS
AWS.config.update({
    accessKeyId: 'AKIA5NXILMPQJDZE4E2E',
    secretAccessKey: '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',
    region: 'us-east-1', // Ejemplo: 'us-east-1'
});

// Crear una nueva instancia de AWS.S3
const bucketName = 'tpfinal-python';
const s3 = new AWS.S3();

// Función para subir imágenes
function uploadImages() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;

    if (files.length === 0) {
        alert('Selecciona al menos una imagen.');
        return;
    }

    const uploadPromises = [];

    for (const file of files) {
        const fileName = file.name;
        const fileKey = 'uploads/' + fileName;

        const params = {
            Bucket: bucketName,
            Key: fileKey,
            Body: file,
            // No incluir ACL aquí para usar la configuración predeterminada del bucket
        };

        uploadPromises.push(s3.upload(params).promise());
    }

    Promise.all(uploadPromises)
        .then(() => {
            alert('Imágenes subidas con éxito.');
            // Recargar las imágenes desde S3
            loadImagesFromS3();
        })
        .catch((error) => {
            console.error('Error al subir imágenes:', error);
            alert('Error al subir imágenes.');
        });
}

// Función para cargar imágenes desde S3
async function loadImagesFromS3() {
    const galleryDiv = document.getElementById('s3-img-gallery');

    try {
        const data = await s3.listObjectsV2({ Bucket: bucketName }).promise();

        // Limpiar la galería antes de agregar nuevas imágenes
        galleryDiv.innerHTML = '';

        // Recorrer objetos en el bucket y agregar imágenes a la galería
        data.Contents.forEach((object) => {
            const imageUrl = s3.getSignedUrl('getObject', { Bucket: bucketName, Key: object.Key });

            const imgElement = document.createElement('img');
            imgElement.src = imageUrl;
            imgElement.alt = '';
            imgElement.onclick = () => openFulImg(imageUrl); // Agregar función para mostrar imagen completa
            galleryDiv.appendChild(imgElement);
        });
    } catch (error) {
        console.error('Error al cargar imágenes desde S3:', error);
    }
}

// Ejecutar la función de carga de imágenes desde S3 al cargar la página
window.onload = loadImagesFromS3;

//Elementos en el DOM

function openFulImg(reference){
    fulImgBox.style.display = "flex";
    fulImg.src = reference
}
function closeImg(){
    fulImgBox.style.display = "none";
}