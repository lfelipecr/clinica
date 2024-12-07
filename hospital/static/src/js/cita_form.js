odoo.define('hospital.cita_form', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');

    publicWidget.registry.CitaForm = publicWidget.Widget.extend({
        selector: '.cita-form',
        events: {
            'change #especialidad': '_onEspecialidadChange',
        },

        _onEspecialidadChange: function (event) {
            console.log('Especialidad seleccionada:', event.target.value); // Debugging
            const especialidadId = event.target.value;
            const medicoSelect = document.querySelector('#medico');

            // Limpiar opciones actuales
            medicoSelect.innerHTML = '<option value="">Seleccione...</option>';

            if (especialidadId) {
                // Hacer solicitud al servidor
                this._rpc({
                    route: '/hospital/obtenermedicos',
                    params: { especialidad_id: especialidadId },
                }).then(function (medicos) {
                    console.log('Médicos obtenidos:', medicos); // Debugging
                    medicos.forEach(function (medico) {
                        const option = document.createElement('option');
                        option.value = medico.id;
                        option.textContent = medico.name;
                        medicoSelect.appendChild(option);
                    });
                }).catch(function (error) {
                    console.error('Error al obtener médicos:', error); // Debugging
                });
            }
        },
    });

    return publicWidget.registry.CitaForm;
});
