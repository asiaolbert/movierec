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
            // childNodes has all data including input, label and text fields,
            // switch below changes the input value to adequate field for later selection
            for(var i=0; i<data["data"].length; i++){
                switch(data["data"][i]){
                    case 1:j=13;
                    break;
                    case 2:j=10;
                    break;
                    case 3:j=7;
                    break;
                    case 4:j=4;
                    break;
                    case 5:j=1;
                }
                document.getElementById(i).childNodes[j].checked=true
            }
})
}