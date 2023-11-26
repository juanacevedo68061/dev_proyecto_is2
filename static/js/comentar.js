$(document).ready(function () {
    // Captura el evento submit del formulario de comentarios
    $('#comentarioForm').submit(function (event) {
        event.preventDefault();  // Evita que se realice la solicitud POST estándar
        var form = $(this);

        // Realiza una solicitud AJAX
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                // Maneja la respuesta del servidor
                if (data.success) {
                    // Si la creación del comentario fue exitosa, puedes realizar acciones adicionales aquí
                    console.log('Comentario creado exitosamente');
                    // Por ejemplo, limpiar el campo de texto
                    $('#id_texto').val('');
                } else {
                    console.log('Error al crear el comentario');
                }
            },
            error: function (data) {
                console.log('Error en la solicitud AJAX');
            }
        });
    });
});
