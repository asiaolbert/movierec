import urllib.parse
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from movierec.algorytmy.content_based import generate_ratings
from movierec.algorytmy.collaborative_filtering import generate_reccomendation
from django.contrib.auth.models import User
import random
import string
from django.http import JsonResponse, HttpResponse
import os
import csv
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_http_methods
import json
import datetime

from .models import Movie, Rating, Recommendation

from django.views.generic import ListView
# Create your views here.
def home_redirect(request):
    return redirect("/home/")
def gen_users(request):
    def get_random_username():
        letters = string.ascii_lowercase
        username = ''.join(random.choice(letters) for i in range(8))
        return username, username + '@gmail.com'

    def get_random_password():
        signs = string.ascii_letters + string.digits
        password = ''.join((random.choice(signs) for i in range(9)))
        return password

    l = []
    for x in range(600):
        l.append([get_random_username()[0], get_random_username()[1], get_random_password()])


    for x in l:
        user = User.objects.create_user(x[0], x[1], x[2])
        user.save()
    return JsonResponse({'ok'})

def read_csv(request):
    path = "/home/asia/pracain/algorytmy/dane"
    os.chdir(path)
    from movierec.models import Movie
    with open('movies.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movie = Movie(movieId=row['movieId'],title=row['title'],genres=row['genres'])
            movie.save()
    return JsonResponse({'ok':1})

def read_csv_rating(request):
    path = "/home/asia/pracain/algorytmy/dane"
    os.chdir(path)
    from movierec.models import Rating
    with open('ratings.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx,row in enumerate(reader):
            connection.cursor().execute(f'INSERT INTO {Rating._meta.db_table} VALUES({idx},{row["userId"]},{row["movieId"]},{row["rating"]},{row["timestamp"]})')
            # rating = Rating(userId=row['userId'],movieId=row['movieId'],rating=row['rating'],timestamp=row['timestamp'])
            # rating.save()
    return JsonResponse({'ok':1})

def home(request):
    return render(request, "movierec/home.html")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'movierec/signup.html', {'form': form})

@login_required
def searchbox(request):
    if 'term' in request.GET:
        movies = Movie.objects.filter(title__istartswith=request.GET.get('term'))
        titles = list()
        for movie in movies:
            titles.append({"label":movie.title,"id":movie.movieId})
        return JsonResponse(titles, safe=False)
    return render(request,"movierec/home.html")

@login_required
def user_rating(request):
    user_id = request.user.id
    movie_id = request.GET["movie_id"]
    rating = Rating.objects.filter(userId=user_id,movieId=movie_id).first()
    if rating==None:
        return JsonResponse({"data":0})
    else:
        return JsonResponse({"data":rating.rating})

@login_required
@require_http_methods(['POST', 'OPTIONS'])
def save_rating(request):
    user_id = request.user.id
    body = json.loads(request.body)
    movie_id = body['movieId']
    rating = body['rating']
    user = User.objects.get(id=user_id)
    movie = Movie.objects.get(movieId=movie_id)
    if Rating.objects.filter(userId = user_id, movieId = movie_id).exists():
        Rating.objects.filter(userId = user_id, movieId = movie_id).update(rating = rating,timestamp=datetime.datetime.now())
        ratings = Rating.objects.filter(userId=user_id).values('userId','movieId', 'rating','timestamp')
        rating = list(ratings)
        recommendations = []
        for row in rating:
            row['timestamp'] = row['timestamp'].timestamp()
            row['userId'] = 0
        print(rating)
        content_recommendations = generate_ratings(rating, 10)
        collaborative_recommendations = generate_reccomendation(rating, 10)
        content=[]
        collaborative=[]
        for x in content_recommendations:
            movie_title = Movie.objects.filter(movieId=int(x)).values('title')[0]['title']
            content.append(movie_title)
        for x in collaborative_recommendations:
            movie_title = Movie.objects.filter(movieId=int(x)).values('title')[0]['title']
            collaborative.append(movie_title)
        recommendations.append({"content_recommendations":content, "collaborative_recommendations":collaborative})

        print(recommendations)
        json_file = json.dumps(recommendations)
        if Recommendation.objects.filter(userId=user_id,recommended_movies=json_file).exists():
            Recommendation.objects.filter(userId=user_id,recommended_movies=json_file).update()
        else:
            Recommendation(userId=user, recommended_movies=json_file).save()
    else:
        Rating(userId = user,movieId=movie,rating=rating,timestamp=datetime.datetime.now()).save()
        ratings = Rating.objects.filter(userId=user_id).values('userId','movieId', 'rating','timestamp')
        rating = list(ratings)
        recommendations = []
        for row in rating:
            row['timestamp'] = row['timestamp'].timestamp()
            row['userId'] = 0
        content_recommendations = generate_ratings(rating, 10)
        collaborative_recommendations = generate_reccomendation(rating, 10)
        content = []
        collaborative = []
        for x in content_recommendations:
            movie_title = Movie.objects.filter(movieId=int(x)).values('title')[0]['title']
            content.append(movie_title)
        for x in collaborative_recommendations:
            movie_title = Movie.objects.filter(movieId=int(x)).values('title')[0]['title']
            collaborative.append(movie_title)
        recommendations.append({"content_recommendations": content,
                                "collaborative_recommendations": collaborative})
        print(recommendations)
        json_file = json.dumps(recommendations)
        if Recommendation.objects.filter(userId=user_id, recommended_movies=json_file).exists():
            Recommendation.objects.filter(userId=user_id, recommended_movies=json_file).update()
        else:
            Recommendation(userId=user, recommended_movies=json_file).save()
    return HttpResponse()
@login_required
def rated_list(request):
    user_id = request.user.id
    ratings = Rating.objects.filter(userId=user_id).values('movieId', 'rating')
    movies =[]
    for movie in ratings:
        movies.append(movie['rating'])
    return JsonResponse({"data": movies})

@login_required
def rated_movies(request):
    user_id = request.user.id
    ratings = Rating.objects.filter(userId=user_id).values('movieId','rating')
    movies=[]
    for movie in ratings:
        main_title = Movie.objects.filter(movieId=movie['movieId']).values('title')
        title = main_title[0]['title'].split(' (')[0]
        url = urlopen("https://api.themoviedb.org/3/search/movie?api_key=493ea9e32e1d2f282c72572e88e8a80f&query=" + urllib.parse.quote(title) + "&callback=?")
        data = url.read().decode('utf-8').strip('?()')
        data=json.loads(data)
        if data["total_results"]==0:
            poster_path="https://via.placeholder.com/542x813.png?text=Sorry+we+couldnt+find+this+poster"
        for i in data["results"]:
            if i["poster_path"] != None:
                poster_path = "http://image.tmdb.org/t/p/w500/" + i["poster_path"]
                break
            else:
                poster_path = "https://via.placeholder.com/542x813.png?text=Sorry+we+couldnt+find+this+poster"
        movies.append({'poster':poster_path,'title':main_title[0]['title'],'rating':movie['rating']})

    return render(request, 'movierec/rated_movies.html', {'movies': movies})
@login_required
@require_http_methods(['POST', 'OPTIONS','GET'])
def recommended_movies(request):
    return render(request,'movierec/recommended_movies.html')

def movie_list(request):
    user_id= request.user.id
    recommendations = Recommendation.objects.latest('id').recommended_movies
    print(recommendations)
    # recommendations = recommendations_object[0]['recommended_movies']
    number_of_rated_movies = Rating.objects.filter(userId=user_id).count()
    min=0
    max=50
    if number_of_rated_movies>max:
        number_of_rated_movies=max
    elif number_of_rated_movies<min:
        number_of_rated_movies=min
    min_max_normalization = (number_of_rated_movies-min)/(max-min)
    default= (min_max_normalization*7)-5
    print(type(json.loads(recommendations)))
    return JsonResponse({"data":json.loads(recommendations),"default":default})
