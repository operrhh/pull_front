function limpiarFormulario() {
  // Limpiar el campo de nombre
  document.getElementById('firstName').value = '';

  document.getElementById('lastName').value = '';

  document.getElementById('personNumber').value = '';

  document.getElementById('base_datos').value = '';

  // Resetear Select2 departamentoDropdown
  $('#departamentoDropdown').val(null).trigger('change');

  document.getElementById('grillaUsuarios').innerHTML = '';
}
