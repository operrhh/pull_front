function inicializarSelectDepartamentos() {
    $('#departamentoDropdown').select2({
        placeholder: 'Seleccione un departamento',
        allowClear: true,
        minimumInputLength: 3,  // Cambiado a 3
        ajax: {
            url: '/works/proxy-departments/',
            dataType: 'json',
            data: function (params) {
                return {
                    base_datos: document.getElementById('base_datos').value.toLowerCase(),
                    name: params.term  // Usa 'name' en lugar de 'search'
                };
            },
            processResults: function (data) {
                return {
                    results: data.items.map(dept => ({ id: dept.dept_id, text: dept.name }))
                };
            }
        }
    });
    var departamentoId = '{{ departamentoId }}';
    if (departamentoId) {
        $('#departamentoDropdown').val(departamentoId).trigger('change');
    }
}

