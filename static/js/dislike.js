document.addEventListener("DOMContentLoaded", function() {
    const dislikeButtons = document.querySelectorAll(".dislike-button");
    const likeButtons = document.querySelectorAll(".like-button");

    dislikeButtons.forEach(dislikeButton => {
        dislikeButton.addEventListener("click", function(event) {
            event.preventDefault();
            const publicacionId = this.dataset.publicacionId;
            const dislikesCount = document.querySelector(`#dislikes-count-${publicacionId}`);
            const likesButton = document.querySelector(`.like-button[data-publicacion-id="${publicacionId}"]`);
            const likesCount = document.querySelector(`#likes-count-${publicacionId}`);

            fetch(`/publicaciones/dislike/${publicacionId}/`)
                .then(response => response.json())
                .then(data => {
                    dislikesCount.textContent = data.dislikes;
                    if (data.ha_dado_dislike) {
                        dislikeButton.classList.add("disliked");
                        // Si tenía un "like", quitarlo y actualizar la cantidad de likes
                        if (data.tiene_like) {
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
