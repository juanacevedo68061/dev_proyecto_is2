$(document).ready(function() {
    $('.btn-estado').on('click', function() {
        var publicacionId = $(this).data('publicacion-id');
        
        $.ajax({
            url: '/publicaciones/estado/' + publicacionId + '/', // URL directa
            method: 'GET',
            success: function(data) {
                if (data.activo) {
                    // Si la publicación está activa
                    $('.btn-estado[data-publicacion-id="'+publicacionId+'"]').html('<i class="fas fa-toggle-on btn-encendido"></i> <span class="descripcion">Inactivar</span>');
                } else {
                    // Si la publicación está inactiva
                    $('.btn-estado[data-publicacion-id="'+publicacionId+'"]').html('<i class="fas fa-toggle-off btn-apagado"></i> <span class="descripcion">Activar</span>');
                }
                $('.btn-estado[data-publicacion-id="'+publicacionId+'"]').data('activo', data.activo);
            }
        });
    });
});
