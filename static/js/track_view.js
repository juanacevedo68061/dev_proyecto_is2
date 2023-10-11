$(document).ready(function() {
    var scrollHeight = $(document).height();
    var winHeight = $(window).height();
    var publicacionId = $("#publicacion-data").data("id"); // Obtiene el valor de id desde el atributo de datos
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val(); // Obtiene el token CSRF

    // Al ingresar a la publicación, borra el valor del almacenamiento local
    localStorage.removeItem("publicacion_" + publicacionId);

    $(window).scroll(function() {
        var scrollPos = $(this).scrollTop();
        var scrollPercentage = (scrollPos / (scrollHeight - winHeight)) * 100;

        // Cuando se alcanza el final de la página
        if (scrollPercentage >= 99 && !localStorage.getItem("publicacion_" + publicacionId)) {
            // Marcar la publicación como "vista" en el almacenamiento local
            localStorage.setItem("publicacion_" + publicacionId, "vista");

            // Realizar la solicitud AJAX y contar la vista
            $.ajax({
                type: "POST",
                url: "/publicaciones/track_view/" + publicacionId + "/",
                data: {
                    csrfmiddlewaretoken: csrfToken
                },
                success: function(data) {
                    // Actualiza la vista en el cliente
                    if (data.status === "success") {
                        console.log("Vista registrada con éxito. Nuevas vistas:", data.views);
                        $("#contador-views").html(data.views);
                    }
                }
            });
        }
    });
});
