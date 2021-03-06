from django.urls import path
from . import views
# from.views import Search


urlpatterns = [

    # path('gen_users/', views.gen_users, name='gen_users'),
    # path('read_csv/', views.read_csv, name='read_csv'),
    # path('read_csv_rating/', views.read_csv_rating, name='read_csv_rating'),
    path('',views.home_redirect, name='home_redirect'),
    path('home/',views.searchbox,name='home'),
    path('user_rating/',views.user_rating,name='user_rating'),
    path('save_rating/',views.save_rating,name='save_rating'),
    path('rated_movies/',views.rated_movies,name='rated_movies'),
    path('rated_list/',views.rated_list, name='rated_list'),
    path('recommended_movies/',views.recommended_movies,name='recommended_movies'),
    path('movie_list/',views.movie_list,name='movie_list'),
    # path('home/',Search.as_view(),name='home'),
    path('signup/', views.signup, name='signup'),

]