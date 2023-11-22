document.addEventListener("DOMContentLoaded", function() {
    const starLinks = document.querySelectorAll(".star-link");
    const calificacionCantidad = document.querySelector("#calificacion-cantidad");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const calificacionMensaje = document.querySelector("#calificacion-mensaje");

    starLinks.forEach(starLink => {
        starLink.addEventListener("click", function(event) {
            event.preventDefault();
            const rating = parseInt(this.getAttribute('data-rating'));
            const publicacionId = this.getAttribute('data-publicacion-id');

            fetch(`/publicaciones/calificar/${publicacionId}/`, {
                method: "POST",
                body: JSON.stringify({ rating: rating }),
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`La solicitud fetch falló con estado ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    calificacionCantidad.textContent = data.calificaciones;
                    mostrarCalificacionMensaje(data.rating);
                    mostrarCalificacionEstrellas(data.rating);
                })
                .catch(error => {
                    console.error("Error en la solicitud fetch:", error);
                });
        });
    });

    // Agregar lógica para cargar la calificación al cargar la página
    const publicacionId = document.querySelector("#calificacion-mensaje").getAttribute("data-id");

    // Realiza una solicitud GET para obtener la calificación actual
    fetch(`/publicaciones/calificar/${publicacionId}/`, {
        method: "GET",
    })
        .then(response => {
            if (!response.ok) {
                throw Error(`La solicitud fetch falló con estado ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            mostrarCalificacionMensaje(data.rating);
            mostrarCalificacionEstrellas(data.rating);
        })
        .catch(error => {
            console.error("Error en la solicitud fetch:", error);
        });

    // Función para mostrar el mensaje de calificación
    function mostrarCalificacionMensaje(rating) {
        if (rating > 0) {
            const estilo = obtenerEstiloCalificacion(rating);
            calificacionMensaje.innerHTML = `<span style="font-size: 20px;">Calificación: <span style="color: ${estilo.color};">${estilo.mensaje}</span></span>`;
        } else {
            calificacionMensaje.innerHTML = "";
        }
    }

    // Función para mostrar las estrellas de calificación
    function mostrarCalificacionEstrellas(rating) {
        starLinks.forEach(starLink => {
            const starRating = parseInt(starLink.getAttribute('data-rating'));
            if (starRating <= rating) {
                starLink.style.color = "yellow"; // Cambia el color de las estrellas a amarillo
            } else {
                starLink.style.color = "gray"; // Cambia el color de las estrellas a gris
            }
        });
    }

    function obtenerEstiloCalificacion(rating) {
        let estilo = { color: "", mensaje: "" };
        switch (rating) {
            case 1:
                estilo.color = "#FF0000";
                estilo.mensaje = "Muy Malo";
                break;
            case 2:
                estilo.color = "#FF4500";
                estilo.mensaje = "Malo";
                break;
            case 3:
                estilo.color = "#D4AF37";
                estilo.mensaje = "Regular";
                break;
            case 4:
                estilo.color = "#008000";
                estilo.mensaje = "Bueno";
                break;
            case 5:
                estilo.color = "#0000FF";
                estilo.mensaje = "Excelente";
                break;
        }
        return estilo;
    }
});
