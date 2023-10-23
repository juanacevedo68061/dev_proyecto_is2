document.addEventListener('DOMContentLoaded', function () {
    var columns = document.querySelectorAll('.kanban-column');

    for (var i = 0; i < columns.length; i++) {
        new Sortable(columns[i], {
            group: 'kanban',
            onEnd: function (evt) {
                var publicacionId = evt.item.querySelector('.sortable-item').id;
                var columnaId = evt.to.id;

                fetch('/kanban/actualizar/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken'), // Agrega el token CSRF
                    },
                    body: 'id_publicacion=' + publicacionId + '&nuevo_estado=' + columnaId,
                })
                .then(response => response.json())
                .then(data => {
                    // Maneja la respuesta del servidor si es necesario
                    console.log(data);
                })
                .catch(error => {
                    // Maneja errores si es necesario
                    console.error('Error:', error);
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
