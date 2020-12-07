document.getElementById("recommendations-container").addEventListener("load", recommendations());

function movie_card(data,i, algo) {
    // console.log(data["data"])
    movie_title = data["data"][0][algo][i]
    film = movie_title.split('(')[0]
    console.log(movie_title)
    $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=493ea9e32e1d2f282c72572e88e8a80f&query=" + film + "&callback=?", function (json) {
        for (var j = 0; j < json.results.length; j++) {
            if (json.results[j].poster_path != null) {
                poster_path = json.results[j].poster_path
                break;
            }
        }
        movie_title2 = data["data"][0][algo][i]
    // console.log(poster_path)
         if (json.total_results !== 0){
    $("#recommended-movies").append('   <div class="col s3">\n' +
        '                    <div class="card blue-grey darken-1">\n' +
        '                        <div class="card-image">\n' +
        '                            <img id="rec-poster"  src=\"http://image.tmdb.org/t/p/w500/' + poster_path + '\">\n' +
        '                        </div>\n' +
        '                        <div class="card-stacked">\n' +
        '                            <div class="card-content">\n' +
        '                                <p id="movie-title2">' + movie_title2 + '</p>\n' +
        '                            </div></div></div></div>')}
         else{
             $("#recommended-movies").append('   <div class="col s3">\n' +
        '                    <div class="card blue-grey darken-1">\n' +
        '                        <div class="card-image">\n' +
        '                            <img id = "no-poster" class="img-resposnive" src=\"https://via.placeholder.com/542x813.png?text=Sorry+we+couldnt+find+this+poster\">\n' +
        '                        </div>\n' +
        '                        <div class="card-stacked">\n' +
        '                            <div class="card-content">\n' +
        '                                <p id="movie-title">' + movie_title2 + '</p>\n' +
        '                            </div></div></div></div>')
         }


})}

function recommendations() {
    fetch('/movie_list', {
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'include'
    })

        .then(response => response.json())
        // .then(data => console.log(data["data"]))
        .then(data => {
            // console.log(data);
                var rangeSlider = document.getElementById('slider-range');
                noUiSlider.create(rangeSlider, {
                    start: [data["default"]],
                    step: 1,
                    range: {
                        'min': [-5],
                        'max': [5]
                    }
                });

                var rangeSliderValueElement = document.getElementById('slider-range-value');

                rangeSlider.noUiSlider.on('update', function (values, handle) {
                    rangeSliderValueElement.innerHTML = values[handle];
                    slider_value = parseInt(values[0]);
                    console.log(slider_value)
                    $('#recommended-movies').empty()

                if (slider_value > 0) {
                    for (var i = 0; i < (5 + slider_value); i++) {
                        movie_card(data,i, "collaborative_recommendations")

                    }
                    for (var i = 0; i < (5 - slider_value); i++) {
                        movie_card(data,i, "content_recommendations")

                    }}
                else
                    {
                        for (var i = 0; i < (5 - slider_value); i++) {
                            movie_card(data,i, "content_recommendations")

                        }
                        for (var j = 0; j < (5 + slider_value); j++) {
                            movie_card(data,j, "collaborative_recommendations")
                        }
                    }});
                }


            //         recommendations.append(content_recommendations[0:(5 + slider_value)])
            //        recommendations.append(collaborative_recomendations[0:(5 - slider_value)])
            //      else:
            //          recommendations.append(content_recommendations[0:(5 - slider_value)])
            // #        recommendations.append(collaborative_recomendations[0:(5 + slider_value)])}

        )
}


// document.getElementById('read-button').addEventListener('click', function () {
//
//     value = rangeSlider.noUiSlider.get()
//     console.log(value);
//
//
// });
