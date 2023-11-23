$(document).ready(function() {
    $('.btn-destacado').on('click', function() {
        var publicacionId = $(this).data('publicacion_id');
        
        $.ajax({
            url: '/publicaciones/estatus/' + publicacionId + '/', // URL directa
            method: 'GET',
            success: function(data) {
                if (data.destacado) {
                    $('.btn-destacado[data-publicacion_id="'+publicacionId+'"]').html('<i class="fas fa-toggle-on btn-encendido-destacado"></i> <span class="descripcion-destacado">Quitar Destacado</span>');
                } else {
                    $('.btn-destacado[data-publicacion_id="'+publicacionId+'"]').html('<i class="fas fa-toggle-off btn-apagado-destacado"></i> <span class="descripcion-destacado">Destacar</span>');
                }
                $('.btn-destacado[data-publicacion_id="'+publicacionId+'"]').data('destacado', data.destacado);
            }
        });
    });
});
