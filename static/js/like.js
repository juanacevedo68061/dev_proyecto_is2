document.addEventListener("DOMContentLoaded", function() {
    const likeButtons = document.querySelectorAll(".like-button");
    const dislikeButtons = document.querySelectorAll(".dislike-button");

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
                    if (data.ha_dado_like) {
                        likeButton.classList.add("liked");
                        // Si tenía un "dislike", quitarlo y actualizar la cantidad de dislikes
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
