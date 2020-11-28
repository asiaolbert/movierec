document.getElementById("rated-movies-container").addEventListener("load", stars());
// console.log("blablabla");
function stars() {
    // alert("goog");
    fetch('/rated_movies/', {
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'include'
    })
        .then(response => response.json())
        .then(console.log("ok"))
}