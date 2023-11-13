document.addEventListener("DOMContentLoaded", function() {
    const favoritoButtons = document.querySelectorAll(".favorito-button");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    favoritoButtons.forEach(favoritoButton => {
        favoritoButton.addEventListener("click", function(event) {
            event.preventDefault();
            const categoriaId = this.dataset.categoriaId;
            const iconFavorito = this.querySelector('.icon-favorito');

            fetch(`/administracion/favorito/${categoriaId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
            })
                .then(response => response.json())
                .then(data => {
                    // Cambiar el ícono y el color según el estado del favorito
                    if (data.favorito) {
                        this.classList.add("favorito");
                        iconFavorito.classList.remove("far");
                        iconFavorito.classList.add("fa");
                        iconFavorito.style.color = "#f91880";  // Puedes ajustar el color según tus preferencias
                    } else {
                        this.classList.remove("favorito");
                        iconFavorito.classList.remove("fa");
                        iconFavorito.classList.add("far");
                        iconFavorito.style.color = "gray";  // Puedes ajustar el color según tus preferencias
                    }
                })
                .catch(error => {
                    console.error("Error en la solicitud fetch:", error);
                });
        });
    });
});
