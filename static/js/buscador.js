document.getElementById("q").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        submitBothForms();
    }
});

function submitBothForms() {
    var q = document.getElementById("q");
    var q_avanzada = document.getElementById("id_q");
    q_avanzada.value = q.value;
    document.getElementById("search-form").submit();
    return true;
}
