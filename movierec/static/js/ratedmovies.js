document.getElementById("rated-movies-container").addEventListener("load", stars());
// console.log("blablabla");
function stars() {
    // alert("goog");
    fetch('/rated_list/', {
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'include'
    })
        .then(response => response.json())
        .then(data => {console.log(data["data"])
            // var elements = document.getElementsByClassName("container-n");

            for(var i=0; i<data["data"].length; i++){
                starsvalue = data["data"][i]
            console.log(document.getElementById(i).children)
                if (starsvalue > 0) {
                    for (var i = 0; i <= starsvalue; i=i+2) {
                        // document.getElementById("star" + i).checked = true;
                        console.log(document.getElementById(i).children[i])
                        document.getElementById("stars-rated-movies"+i).childNodes[i].style.checked=true;
                    }
                }}
})
}