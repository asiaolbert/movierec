document.getElementById("movie-container").style.visibility = "hidden";
$(function () {
    $('#title').autocomplete({
        source: '/home/',
        select: function (event, ui) {
            AutoCompleteSelectHandler(event, ui)
        },
        minLength: 2,

    });
});

function AutoCompleteSelectHandler(event, ui) {
    var selectedObj = ui.item;
    {
        console.log(selectedObj);

    }
    if (selectedObj) {
        fetch('/user_rating/?movie_id=' + selectedObj.id, {
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'include'
        })


            .then(response => response.json())
            .then(data => {
                document.getElementById("movie-container").style.visibility = "visible";
                $("#movie-title").text(selectedObj.label);
                starsvalue = data["data"]
                if (starsvalue > 0) {
                    for (var i = 1; i <= starsvalue; i++) {
                        document.getElementById("star" + i).checked = true;
                    }
                }
                // if(data["data"]>0){
                //     $("#rating").text("You have already rated this film for: " + data["data"]);
                //     $("#exp").text("You can change your rating by choosing a star below.")
                // }

            })

        $(':radio').change(function () {
            // console.log('New star rating: ' + this.value);
            rating = this.value;
            console.log(rating);
            if (rating) {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = cookies[i].trim();
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }

                fetch('/save_rating/', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        "X-CSRFToken": getCookie('csrftoken'),
                    },
                    credentials: 'same-origin',
                    body: JSON.stringify({'movieId': selectedObj.id, 'rating': rating}),
                    // body:data
                })
                    .then(response => response.json())
                    .then($("#send-text").text("Your rating is saved!"))

            }
        });
        var film = selectedObj.label.split('(')[0]

        $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=493ea9e32e1d2f282c72572e88e8a80f&query=" + film + "&callback=?", function (json) {
            var i;
            for (i = 0; i < json.results.length; i++) {
                if (json.results[i].poster_path != null) {
                    var poster_path = json.results[i].poster_path
                    {
                        break;
                    }
                }
            }
            if (json.total_results !== 0) {
                console.log(json);
                $('#poster').html('<img src=\"http://image.tmdb.org/t/p/w500/' + poster_path + '\" class=\"img-responsive\" >');
            } else {
                $('#poster').html('<p>No image found</p>')
            }
        })

    }
}








