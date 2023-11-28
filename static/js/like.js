document.addEventListener("DOMContentLoaded", function() {
    const likeButtons = document.querySelectorAll(".like-button");

    likeButtons.forEach(likeButton => {
        likeButton.addEventListener("click", function(event) {
            event.preventDefault();
            const publicacionId = this.dataset.publicacionId;
            const likesCount = document.querySelector(`#likes-count-${publicacionId}`);
            const dislikesButton = document.querySelector(`.dislike-button[data-publicacion-id="${publicacionId}"]`);
            const dislikesCount = document.querySelector(`#dislikes-count-${publicacionId}`);

            fetch(`/publicaciones/like/${publicacionId}/`)
                .then(response => response.json())
                .then(data => {
                    likesCount.textContent = data.likes;

                    // if (data.ha_dado_like !== undefined) {
                    //     // Envío del evento a Google Analytics
                    //     gtag('event', 'like', {
                    //         'event_category': 'Interacción',
                    //         'event_label': 'Publicación ' + publicacionId,
                    //         'value': data.ha_dado_like ? 1 : 0  // '1' para like, '0' para unlike.
                    //     });
                    // }

                    if (data.ha_dado_like) {
                        likeButton.classList.add("liked");
                        if (data.tiene_dislike) {
                            dislikesButton.classList.remove("disliked");
                            dislikesCount.textContent = data.dislikes;
                        }
                    } else {
                        likeButton.classList.remove("liked");
                    }
                })
                .catch(error => {
                    console.error("Error en la solicitud fetch:", error);
                });
        });
    });
});
