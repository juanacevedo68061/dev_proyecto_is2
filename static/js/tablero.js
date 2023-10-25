document.addEventListener('DOMContentLoaded', function () {
    var isSubmitting = false;
    var motivoSubmitted = false;  // Bandera para rastrear si se ha enviado el motivo
    var reloadingColumns = false;  // Bandera para rastrear si las columnas se están recargando
    var isUpdating = false;  // Bandera para rastrear si ya se está actualizando

    function reloadColumns() {
        if (reloadingColumns) {
            return;
        }
        reloadingColumns = true;
        $.ajax({
            url: '/kanban/',
            type: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Marca la solicitud como AJAX
            },
            success: function (response) {
                // Reemplaza el contenido de las columnas con el nuevo contenido
                $('.kanban-column').each(function (index, column) {
                    var newContent = $(response).find('#' + column.id).html();
                    $(column).html(newContent);
                });
                reloadingColumns = false;  // Restablecer la bandera
            },
            error: function (error) {
                console.error('Error al cargar los datos:', error);
                reloadingColumns = false;  // Restablecer la bandera en caso de error
            }
        });
    }

    var columns = document.querySelectorAll('.kanban-column');
    for (var i = 0; i < columns.length; i++) {

        new Sortable(columns[i], {
            group: 'kanban',
            onEnd: function (evt) {
                var semaforo = evt.item.getAttribute('color');
                console.log(semaforo)        
                if (semaforo === "verde") {        
                    if (isSubmitting || isUpdating) {
                        return;
                    }

                    isUpdating = true;  // Marcar que se está actualizando

                    var publicacionId = evt.item.id;
                    var columnaId = evt.to.id;

                    clearModal();

                    fetch('/kanban/actualizar/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': getCookie('csrftoken'),
                        },
                        body: 'id_publicacion=' + publicacionId + '&nuevo_estado=' + columnaId,
                    })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Respuesta de la solicitud de actualizar:', data);
                            if (data.vuelve===true) {
                                reloadColumns();
                            }
                            if (data.message) {
                                console.log(data.message);
                            }

                            if (data.reason_required) {
                                $('#motivoModal').modal('show');

                                var guardarMotivoBtn = document.getElementById('guardarMotivoBtn');
                                guardarMotivoBtn.addEventListener('click', function () {
                                    var motivo = document.getElementById('motivoInput').value;
                                    var columnaId = evt.to.id;
                                    console.log('Columna destino:', columnaId);
                                    $('#motivoModal').modal('hide');

                                    if (!motivoSubmitted) {
                                        motivoSubmitted = true;

                                        fetch('/kanban/motivo/', {
                                            method: 'POST',
                                            headers: {
                                                'Content-Type': 'application/x-www-form-urlencoded',
                                                'X-CSRFToken': getCookie('csrftoken'),
                                            },
                                            body: 'id_publicacion=' + publicacionId + '&motivo=' + motivo + '&nuevo=' + columnaId,
                                        })
                                            .then(response => response.json())
                                            .then(data => {
                                                console.log('Respuesta de la solicitud de motivo:', data);

                                                var motivoInput = document.getElementById('motivoInput');
                                                motivoInput.value = '';

                                                if (data.vuelve === true) {
                                                    reloadColumns();
                                                }

                                                isUpdating = false;  // Restablecer la bandera
                                                motivoSubmitted = false;  // Restablecer la bandera
                                            })
                                            .catch(error => {
                                                console.error('Error:', error);
                                                isUpdating = false;  // Restablecer la bandera
                                                motivoSubmitted = false;  // Restablecer la bandera
                                            });
                                    }
                                });
                            } else {
                                isUpdating = false;  // Restablecer la bandera
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            isUpdating = false;  // Restablecer la bandera
                        });
                } else {
                    console.log("No está en color verde: queda todo desabilitado");
                    reloadColumns();
                }
            }
        });
    }
});

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function clearModal() {
    var motivoInput = document.getElementById('motivoInput');
    motivoInput.value = '';
}