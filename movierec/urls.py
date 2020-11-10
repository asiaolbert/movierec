from django.urls import path
from . import views
# from.views import Search


urlpatterns = [

    # path('gen_users/', views.gen_users, name='gen_users'),
    # path('read_csv/', views.read_csv, name='read_csv'),
    # path('read_csv_rating/', views.read_csv_rating, name='read_csv_rating')
    path('home/',views.searchbox,name='home'),
    # path('home/',Search.as_view(),name='home'),
    path('signup/', views.signup, name='signup'),

]