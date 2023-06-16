// Array de nombres de archivo de imágenes en la carpeta
var imagenes = [
    "ralsei.png",
    "deltarune_crew.png"
];
  
// Índice de la imagen actual
var indice = 0;

// Tamaño máximo para las imágenes (ajusta según tus necesidades)
var tamanoMaximo = 400; // en píxeles
  
// Función para cambiar la imagen
function cambiarImagen() {
    // Obtener el elemento img por su id
    var img = document.getElementById("imagen-ralsei");
  
    // Cambiar la ruta de origen de la imagen
    img.src = "/home/juanjo/Escritorio/Projects/LabRedes2/Images/" + imagenes[indice];

    // Reescalar la imagen si excede el tamaño máximo
    if (img.width > tamanoMaximo || img.height > tamanoMaximo) {
        if (img.width > img.height) {
            img.height = tamanoMaximo;
            img.width = "auto";
        }else {
            img.width = tamanoMaximo;
            img.height = "auto";
        }
    }
  
    // Incrementar el índice para obtener la siguiente imagen
    indice++;
  
    // Si el índice supera la longitud del array, volver al inicio
    if (indice == imagenes.length) {
      indice = 0;
    }
}
  
// Obtener el elemento img por su id
var img = document.getElementById("imagen-ralsei");

// Agregar un event listener al hacer clic en la imagen
img.addEventListener("click", cambiarImagen);
  