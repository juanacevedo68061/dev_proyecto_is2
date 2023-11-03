document.addEventListener("DOMContentLoaded", function () {
    var compartirBtn = document.querySelector('.compartir-btn');
    var modal = document.getElementById('qrModal');
    var qrImage = document.getElementById('qrImage');
    var closeModalBtn = document.querySelector('.close-modal');

    compartirBtn.addEventListener('click', function (event) {
        // Obtén la URL de generación del código QR
        var qrUrl = this.getAttribute('href');

        // Configura la imagen del código QR en el modal
        qrImage.src = qrUrl;

        // Muestra el modal
        modal.style.display = 'block';

        // Obtén el ID de publicacion desde el atributo de datos
        var publicacionId = this.getAttribute('data-publicacion-id');

        // Evita que el enlace se abra en una nueva pestaña
        event.preventDefault();

        // Realiza una solicitud AJAX para obtener la cantidad actualizada de compartidos
        fetch(`/publicaciones/compartidas/${publicacionId}/`)
            .then(response => {
                // Imprime un mensaje para verificar que la solicitud se realizó correctamente
                console.log('Solicitud de AJAX realizada con éxito');

                return response.json();
            })
            .then(data => {
                // Imprime la respuesta JSON en la consola para verificar
                console.log('Respuesta JSON:', data);

                // Actualiza la cantidad de compartidos en el span utilizando el campo 'shared_count' de la respuesta JSON
                var sharedCountSpan = document.getElementById('shared_count');
                sharedCountSpan.textContent = data.shared_count;

                // Actualiza el atributo de datos con el nuevo valor
                sharedCountSpan.setAttribute('data-publicacion-shared', data.shared_count);

                // Imprime un mensaje para verificar que la actualización se realizó correctamente
                console.log('Cantidad de compartidos actualizada en el HTML:', data.shared_count);

            })
            .catch(error => {
                // Imprime cualquier error en la consola para verificar
                console.error('Error al obtener la cantidad de compartidos:', error);
            });


    });

    closeModalBtn.addEventListener('click', function () {
        // Cierra el modal al hacer clic en el botón "x"
        modal.style.display = 'none';
    });

    // Evita que el modal se cierre al hacer clic fuera del contenido del modal
    modal.addEventListener('click', function (event) {
        event.stopPropagation();
    });

});
