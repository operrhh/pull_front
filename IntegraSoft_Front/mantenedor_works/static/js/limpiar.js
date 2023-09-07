// Función para limpiar el formulario y los valores en localStorage
function limpiarFormulario() {
  const person_numberInput = document.getElementById("person_number");
  const nombreInput = document.getElementById("nombre");
  const apellidosInput = document.getElementById("apellidos");
  const ciudadInput = document.getElementById("ciudad");
  const baseDatosSelect = document.getElementById("base_datos");

//   Limpiar los valores de los campos del formulario
  person_numberInput.value = "";
  nombreInput.value = "";
  apellidosInput.value = "";
  ciudadInput.value = "";
  baseDatosSelect.value = "PeopleSoft"; // Establecer el valor predeterminado

  // Eliminar los valores en localStorage
  localStorage.removeItem("person_number");
  localStorage.removeItem("nombre");
  localStorage.removeItem("apellidos");
  localStorage.removeItem("ciudad");
  localStorage.removeItem("base_datos");
}
