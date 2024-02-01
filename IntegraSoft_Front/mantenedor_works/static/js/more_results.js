// document.addEventListener('DOMContentLoaded', function() {
//     var botonCargarMas = document.getElementById('cargar-mas');

//     if (botonCargarMas) {
//         botonCargarMas.addEventListener('click', function(event) {
//             event.preventDefault();
//             var nextUrl = botonCargarMas.getAttribute('data-next-url');

//             fetch(`/works/cargar_mas_usuarios/?next_url=${encodeURIComponent(nextUrl)}&base_datos=${baseDatos}`)
//                 .then(response => response.json())
//                 .then(data => {
//                     console.log("Datos recibidos:", data);

//                     if (data.error) {
//                         console.error('Error:', data.error);
//                         return;
//                     }

//                     var tabla = document.getElementById('tabla-resultados').getElementsByTagName('tbody')[0];
//                     var usuarios = data.items || data.results; // Asumiendo que HCM usa 'items' y PeopleSoft 'results'

//                     if (usuarios && Array.isArray(usuarios)) {
//                         usuarios.forEach(usuario => {
//                             var fila = tabla.insertRow();
//                             fila.insertCell(0).innerHTML = usuario.person_number || usuario.emplid; // Asegúrate de ajustar según la respuesta de cada API
//                             fila.insertCell(1).innerHTML = usuario.display_name || usuario.name; // Ajustar según sea necesario
//                             fila.insertCell(2).innerHTML = usuario.department_name || usuario.dept_descr; // Ajustar según sea necesario

//                             var celdaAcciones = fila.insertCell(3);
//                             var urlDetalle = `/works/detalles/${baseDatos}/${usuario.person_number || usuario.emplid}/`;
//                             celdaAcciones.innerHTML = `<a href="${urlDetalle}" class="btn btn-detalle">Ver Detalle</a>`;
//                         });

//                         if (data.next) {
//                             botonCargarMas.setAttribute('data-next-url', data.next);
//                         } else {
//                             botonCargarMas.style.display = 'none';
//                         }
//                     } else {
//                         console.log('No se encontraron usuarios para mostrar.');
//                     }
//                 })
//                 .catch(error => console.error('Error:', error));
//         });
//     }
// });

document.addEventListener('DOMContentLoaded', function() {
    var botonCargarMas = document.getElementById('cargar-mas');
    var loadingSpinner = document.getElementById('loading-spinner'); // Asegúrate de que este ID coincida con tu spinner en HTML

    if (botonCargarMas) {
        botonCargarMas.addEventListener('click', function(event) {
            event.preventDefault();
            var nextUrl = botonCargarMas.getAttribute('data-next-url');

            // Mostrar el spinner y deshabilitar el botón
            loadingSpinner.style.display = 'block';
            botonCargarMas.disabled = true;

            fetch(`/works/cargar_mas_usuarios/?next_url=${encodeURIComponent(nextUrl)}&base_datos=${baseDatos}`)
                .then(response => response.json())
                .then(data => {
                    // Ocultar el spinner y habilitar el botón
                    loadingSpinner.style.display = 'none';
                    botonCargarMas.disabled = false;

                    console.log("Datos recibidos:", data);

                    if (data.error) {
                        console.error('Error:', data.error);
                        return;
                    }

                    var tabla = document.getElementById('tabla-resultados').getElementsByTagName('tbody')[0];
                    var usuarios = data.items || data.results; // Asumiendo que HCM usa 'items' y PeopleSoft 'results'

                    if (usuarios && Array.isArray(usuarios)) {
                        usuarios.forEach(usuario => {
                            var fila = tabla.insertRow();
                            fila.insertCell(0).innerHTML = usuario.person_number || usuario.emplid; // Asegúrate de ajustar según la respuesta de cada API
                            fila.insertCell(1).innerHTML = usuario.display_name || usuario.name; // Ajustar según sea necesario
                            fila.insertCell(2).innerHTML = usuario.department_name || usuario.dept_descr; // Ajustar según sea necesario

                            var celdaAcciones = fila.insertCell(3);
                            var urlDetalle = `/works/detalles/${baseDatos}/${usuario.person_number || usuario.emplid}/`;
                            celdaAcciones.innerHTML = `<a href="${urlDetalle}" class="btn btn-detalle">Ver Detalle</a>`;
                        });

                        if (data.next) {
                            botonCargarMas.setAttribute('data-next-url', data.next);
                        } else {
                            botonCargarMas.style.display = 'none';
                        }
                    } else {
                        console.log('No se encontraron usuarios para mostrar.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Ocultar el spinner y habilitar el botón si hay un error
                    loadingSpinner.style.display = 'none';
                    botonCargarMas.disabled = false;
                });
        });
    }
});
