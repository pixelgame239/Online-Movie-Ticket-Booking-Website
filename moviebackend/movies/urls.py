from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('cinemas/<int:pk>/', views.cinema_detail, name='cinema_detail'),
]
