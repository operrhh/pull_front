  // formulario.js

// Obtener los elementos de entrada de texto y el select
const personNumberInput = document.getElementById("person_number");
const nombreInput = document.getElementById("nombre");
const apellidosInput = document.getElementById("apellidos");
const ciudadInput = document.getElementById("ciudad");
const baseDatosSelect = document.getElementById("base_datos");

// Recuperar los valores de los campos desde localStorage
const storedPersonNumber = localStorage.getItem("person_number");
const storedNombre = localStorage.getItem("nombre");
const storedApellidos = localStorage.getItem("apellidos");
const storedCiudad = localStorage.getItem("ciudad");
const storedBaseDatos = localStorage.getItem("base_datos");

// Establecer los valores de los campos con los valores almacenados
if (storedPersonNumber) {
  personNumberInput.value = storedPersonNumber;
}
if (storedNombre) {
  nombreInput.value = storedNombre;
}
if (storedApellidos) {
  apellidosInput.value = storedApellidos;
}
if (storedCiudad) {
  ciudadInput.value = storedCiudad;
}
if (storedBaseDatos) {
  baseDatosSelect.value = storedBaseDatos;
}
