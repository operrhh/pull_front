// funciona
function habilitarCampos() {
    let baseDatos = document.getElementById('base_datos').value;
    let campos = document.querySelectorAll('#Person_Number, #nombre, #BusinessUnitName, #DepartmentName');
    let mensaje = document.getElementById('mensaje');
    
    campos.forEach(campo => {
        campo.disabled = !baseDatos;
    });

    if (!baseDatos) {
        mensaje.style.display = 'inline';
        mensaje.style.opacity = '1';
        setTimeout(() => {
            mensaje.style.opacity = '0';
            setTimeout(() => {
                mensaje.style.display = 'none';
            }, 2000);  // Espera 2 segundos después de que la opacidad llegue a 0 para ocultar el mensaje
        }, 5000);
    } else {
        mensaje.style.display = 'none';
    }
}

// Llamada inicial para establecer el estado correcto de los campos y mostrar el mensaje
habilitarCampos();
