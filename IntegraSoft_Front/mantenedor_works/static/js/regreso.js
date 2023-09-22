//funciona
document.addEventListener("DOMContentLoaded", function () {
    const retrocederButton = document.getElementById("regresar_formulario");
    
    if (retrocederButton) {
      // Agregar un controlador de eventos al botón o enlace
      retrocederButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevenir el comportamiento predeterminado del enlace (navegación)
  
        // Usar el objeto History para retroceder en la historia del navegador
        window.history.back();
      });
    }
  });
  