// JavaScript para mostrar el modal
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

        // Evita que el enlace se abra en una nueva pestaña
        event.preventDefault();
    });

    closeModalBtn.addEventListener('click', function () {
        // Cierra el modal al hacer clic en el botón "x"
        modal.style.display = 'none';

        // Recarga la página después de cerrar el modal
        location.reload();
    });

    // Evita que el modal se cierre al hacer clic fuera del contenido del modal
    modal.addEventListener('click', function (event) {
        event.stopPropagation();
    });

    window.addEventListener('click', function (event) {
        // Cierra el modal al hacer clic en cualquier parte fuera del contenido del modal
        if (event.target === modal && event.target !== qrImage) {
            modal.style.display = 'none';

            // Recarga la página después de cerrar el modal
            location.reload();
        }
    });
});
