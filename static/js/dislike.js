document.addEventListener("DOMContentLoaded", function() {
    const dislikeButtons = document.querySelectorAll(".dislike-button");

    dislikeButtons.forEach(dislikeButton => {
        dislikeButton.addEventListener("click", function(event) {
            event.preventDefault();
            const publicacionId = this.dataset.publicacionId;
            const dislikesCount = document.querySelector(`#dislikes-count-${publicacionId}`);

            fetch(`/publicaciones/dislike/${publicacionId}/`)
                .then(response => response.json())
                .then(data => {
                    dislikesCount.textContent = data.dislikes;
                    if (data.ha_dado_dislike) {
                        dislikeButton.classList.add("disliked");
                        sendDislikeEvent(publicacionId);
                        if (data.tiene_like) {
                            const likesButton = document.querySelector(`.like-button[data-publicacion-id="${publicacionId}"]`);
                            const likesCount = document.querySelector(`#likes-count-${publicacionId}`);
                            likesButton.classList.remove("liked");
                            likesCount.textContent = data.likes;
                        }
                    } else {
                        dislikeButton.classList.remove("disliked");
                    }
                })
                .catch(error => {
                    console.error("Error en la solicitud fetch:", error);
                });
        });
    });
});

// Definición de la función sendDislikeEvent
function sendDislikeEvent(publicacionId) {
    gtag('event', 'dislike', {
        'event_category': 'Interacción',
        'event_label': 'Publicación ' + publicacionId,
        'value': 1
    });
    console.log("Evento de dislike enviado para la publicación:", publicacionId);
}
