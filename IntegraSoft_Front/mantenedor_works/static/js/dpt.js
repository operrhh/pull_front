document.addEventListener('DOMContentLoaded', function() {
    let baseDatosSelect = document.getElementById('base_datos');
    if (baseDatosSelect) {
        baseDatosSelect.addEventListener('change', cargarDepartamentos);
    } else {
        console.error("Elemento 'base_datos' no encontrado en el DOM");
    }
});

function cargarDepartamentos(departamentoIdSeleccionado = '') {
    let baseDatos = document.getElementById('base_datos').value.toLowerCase();
    let url = `/works/proxy-departments/?base_datos=${baseDatos}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en la respuesta del servidor: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            let departamentoDropdown = document.getElementById('departamentoDropdown');
            departamentoDropdown.innerHTML = '';

            // Añadir opción por defecto
            let opcionPorDefecto = new Option('Seleccione un departamento', '');
            departamentoDropdown.add(opcionPorDefecto);

            data.departments.forEach(dept => {
                let option = new Option(dept.name, dept.dept_id);
                departamentoDropdown.add(option);
            });

            // Seleccionar automáticamente el departamento si se ha pasado un id, o la opción por defecto
            if (departamentoIdSeleccionado && departamentoIdSeleccionado !== '') {
                departamentoDropdown.value = departamentoIdSeleccionado;
            } else {
                departamentoDropdown.value = ''; // Selecciona la opción por defecto
            }
        })
        .catch(error => console.error('Error:', error));
}

function buscarTrabajadores() {
    let baseDatos = document.getElementById('base_datos').value.toLowerCase();
    let departamentoId = document.getElementById('departamentoDropdown').value; // Obtiene el dept_id

    let url = `/ruta-para-buscar-trabajadores/?base_datos=${baseDatos}`;

    if (departamentoId) {
        url += `&department=${departamentoId}`;
    }

}
