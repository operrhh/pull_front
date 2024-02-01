function habilitarCampos() {
    let baseDatos = document.getElementById('base_datos').value;
    let campos = document.querySelectorAll('#personNumber, #firstName, #lastName, #departamentoDropdown');
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
            }, 2000);
        }, 5000);
    } else {
        mensaje.style.display = 'none';

        // Verifica si Select2 está inicializado antes de destruirlo
        if ($('#departamentoDropdown').data('select2')) {
            $('#departamentoDropdown').select2('destroy');
        }
        
        inicializarSelectDepartamentos();
    }
}

// Llamada inicial para establecer el estado correcto de los campos y mostrar el mensaje
habilitarCampos();
