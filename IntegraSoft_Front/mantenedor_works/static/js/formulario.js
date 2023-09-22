function cargarOpcionesPorBase(baseDatosSeleccionada) {
    fetch(`obtener_opciones_por_base?base_datos=${baseDatosSeleccionada}`)
        .then(response => response.json())
        .then(data => {
            const dropdownUnidades = document.getElementById('BusinessUnitName');
            const dropdownDepartamentos = document.getElementById('DepartmentName');
            
            // Guardar los valores seleccionados previamente
            const unidadSeleccionada = dropdownUnidades.value;
            const departamentoSeleccionado = dropdownDepartamentos.value;
            
            // Limpiar dropdowns
            dropdownUnidades.innerHTML = '<option value="">Seleccione una opción</option>';
            dropdownDepartamentos.innerHTML = '<option value="">Seleccione una opción</option>';
            
            // Llenar dropdowns con los datos recibidos
            data.opciones_unidad_negocio.forEach(unidad => {
                const option = document.createElement('option');
                option.value = unidad;
                option.textContent = unidad;
                dropdownUnidades.appendChild(option);
            });
            
            data.opciones_departamento.forEach(departamento => {
                const option = document.createElement('option');
                option.value = departamento;
                option.textContent = departamento;
                dropdownDepartamentos.appendChild(option);
            });

            // Restaurar los valores seleccionados previamente
            dropdownUnidades.value = unidadSeleccionada;
            dropdownDepartamentos.value = departamentoSeleccionado;
        });
}

const dropdownBaseDatos = document.getElementById('base_datos');
dropdownBaseDatos.addEventListener('change', () => {
    const baseDatosSeleccionada = dropdownBaseDatos.value;
    cargarOpcionesPorBase(baseDatosSeleccionada);
});

// Llamada inicial para cargar las opciones de los dropdowns
const baseDatosSeleccionada = dropdownBaseDatos.value;
cargarOpcionesPorBase(baseDatosSeleccionada);
