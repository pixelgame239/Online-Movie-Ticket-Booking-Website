from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Movie
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),

    # Cinema
    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('cinemas/<int:pk>/', views.cinema_detail, name='cinema_detail'),

    # Ticket
    path('buy_ticket/', views.buy_ticket, name='buy_ticket'),
]
