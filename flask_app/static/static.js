// Gets movies genre list
// https://api.themoviedb.org/3/genre/movie/list?api_key=203336aef5e949156c0daf7b699052dd&language=en-US

// Get image by movie id
// https://api.themoviedb.org/3/movie/{movie_id}/images?api_key=203336aef5e949156c0daf7b699052dd&language=en-US

// Get Movies by keyword
// https://api.themoviedb.org/3/keyword/{keyword_id}/movies?api_key=203336aef5e949156c0daf7b699052dd&language=en-US&include_adult=false

//Get by person
//https://api.themoviedb.org/3/person/{person_id}?api_key=203336aef5e949156c0daf7b699052dd&language=en-US

// Get by popular (generic search screen load in)
// /discover/movie?sort_by=popularity.desc

// Search by movie
// https://api.themoviedb.org/3/search/movie?api_key=203336aef5e949156c0daf7b699052dd&language=en-US&query=&page=1&include_adult=false

// Search by person
// https://api.themoviedb.org/3/search/person?${APIKEY}&language=en-US&query=&page=1&include_adult=false

// Base URL
// https://api.themoviedb.org/3/

// img = poster_path
// genre = genre_ids
// discription = overview
// title = title

const BASEURL = "https://api.themoviedb.org/3/";
const APIKEY = "api_key=203336aef5e949156c0daf7b699052dd";
const POP_URL = BASEURL+'/discover/movie?sort_by=popularity.desc&'+APIKEY;
const IMG_URL = "https://image.tmdb.org/t/p/w500/"+APIKEY;



fetch(`https://api.themoviedb.org/3/search/movie?api_key=203336aef5e949156c0daf7b699052dd&language=en-US&query=Tenacious&page=1&include_adult=false`)
    .then(response => response.json() )
    .then(coderData => console.log(coderData) )
    .catch(err => console.log(err))