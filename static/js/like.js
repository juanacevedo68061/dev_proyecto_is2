document.addEventListener("DOMContentLoaded", function() {
    const likeButtons = document.querySelectorAll(".like-button");

    likeButtons.forEach(likeButton => {
        likeButton.addEventListener("click", function(event) {
            event.preventDefault();
            const publicacionId = this.dataset.publicacionId;
            const likesCount = document.querySelector(`#likes-count-${publicacionId}`);
            const hasLiked = likeButton.classList.contains("liked");

            fetch(`/publicaciones/like/${publicacionId}/`)
                .then(response => response.json())
                .then(data => {
                    likesCount.textContent = data.likes;
                    if (data.ha_dado_like) {
                        likeButton.classList.add("liked");
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
