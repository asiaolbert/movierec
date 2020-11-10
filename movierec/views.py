from django.shortcuts import render
from django.contrib.auth.models import User
import random
import string
from django.http import JsonResponse
import os
import csv
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Movie
from django.views.generic import ListView
# Create your views here.
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
    return render(request, "home.html")

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
    return render(request, 'signup.html', {'form': form})


def searchbox(request):
    if 'term' in request.GET:
        movies = Movie.objects.filter(title__istartswith=request.GET.get('term'))
        titles = list()
        for movie in movies:
            titles.append(movie.title)
        return JsonResponse(titles)
    return render(request,"home.html")

# class Search(ListView):
#     model=Movie
#     template_name = 'home.html'
#     def searchbox(self):
#         query = self.request.GET.get('title')
#         movie_list = Movie.objects.filter(title__icontains=query)
#         return movie_list