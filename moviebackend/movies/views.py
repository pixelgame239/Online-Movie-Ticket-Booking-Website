from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Movie, Cinema, Showtime, Genre

def home(request):
    currentDate = timezone.now()
    showTimesUpNext = Showtime.objects.filter(show_time__gte=currentDate)
    movie_id_up_next = list(showTimesUpNext.values_list('movie_id', flat=True))
    movies_now_showing = Movie.objects.filter(id__in=showTimesUpNext.values('movie_id')).distinct()
    movies_hot = Movie.objects.filter(buy_count__gt=0).order_by('-buy_count')[:3]
    return render(request, 'index.html', {'movies_now_showing': movies_now_showing, "movies_hot": movies_hot})
def movie_list(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()

    query = request.GET.get('q')
    genre = request.GET.get('genre')

    if query:
        movies = movies.filter(title__icontains=query)
    if genre:
        movies = movies.filter(genre=genre)

    return render(request, 'movie_list.html', {
        'movies': movies,
        'genres': genres
    })


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    showtimes = movie.showtimes.all()
    return render(request, 'movie_detail.html', {
        'movie': movie,
        'showtimes': showtimes
    })
def cinema_list(request):
    cinemas = Cinema.objects.all().prefetch_related("showtimes__movie")

    for cinema in cinemas:
        showtimes = cinema.showtimes.all()
        cinema.movies_list = list(set([s.movie.title for s in showtimes]))
        cinema.showtime_count = showtimes.count()

    return render(request, "cinema_list.html", {"cinemas": cinemas})
def cinema_detail(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    showtimes = cinema.showtimes.select_related('movie').order_by('show_time')
    return render(request, 'cinema_detail.html', {
        'cinema': cinema,
        'showtimes': showtimes
    })


@login_required
@user_passes_test(admin_required)
def showtime_create(request):
    if request.method == 'POST':
        form = ShowtimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = ShowtimeForm()
    return render(request, 'showtime_form.html', {'form': form})