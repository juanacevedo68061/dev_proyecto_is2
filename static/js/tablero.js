document.addEventListener('DOMContentLoaded', function () {
    var columns = document.querySelectorAll('.kanban-column');
    var isSubmitting = false;

    for (var i = 0; i < columns.length; i++) {
        new Sortable(columns[i], {
            group: 'kanban',
            onEnd: function (evt) {
                if (isSubmitting) {
                    return;
                }

                isSubmitting = true;

                var publicacionId = evt.item.querySelector('.sortable-item').id;
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
                    console.log(data);

                    if (data.reason_required) {
                        $('#motivoModal').modal('show');

                        var guardarMotivoBtn = document.getElementById('guardarMotivoBtn');
                        guardarMotivoBtn.addEventListener('click', function() {
                            var motivo = document.getElementById('motivoInput').value;
                            var columnaId = evt.to.id;
                            $('#motivoModal').modal('hide');

                            fetch('/kanban/motivo/', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                    'X-CSRFToken': getCookie('csrftoken'),
                                },
                                body: 'id_publicacion=' + publicacionId + '&motivo=' + motivo + '&nuevo='+ columnaId,
                            })
                            .then(response => response.json())
                            .then(data => {
                                console.log(data);

                                var motivoInput = document.getElementById('motivoInput');
                                motivoInput.value = '';

                                if (data.reason_required === false) {
                                    location.reload(); // Recarga la página si no se requiere motivo
                                }

                                isSubmitting = false;
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                isSubmitting = false;
                            });
                        });
                    } else {
                        isSubmitting = false;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    isSubmitting = false;
                });
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
