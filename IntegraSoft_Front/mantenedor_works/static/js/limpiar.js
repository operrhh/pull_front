function limpiarFormulario() {
  // Limpiar el campo de nombre
  document.getElementById('firstName').value = '';

  document.getElementById('lastName').value = '';

  document.getElementById('personNumber').value = '';

  document.getElementById('base_datos').value = '';

  document.getElementById('departamentoDropdown').value = '';

  document.getElementById('grillaUsuarios').innerHTML = '';
}
