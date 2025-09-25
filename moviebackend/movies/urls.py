from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    path('', views.home, name='home'),
    path('movies_list/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('cinemas/<int:pk>/', views.cinema_detail, name='cinema_detail'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('create/', views.movie_create, name='movie_create'),
    path('<int:pk>/update/', views.movie_update, name='movie_update'),
    path('<int:pk>/delete/', views.movie_delete, name='movie_delete'),
    path('showtime/create/', views.showtime_create, name='showtime_create'),
]
