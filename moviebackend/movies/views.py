from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Movie, Cinema, Showtime, Genre
from .forms import MovieForm, ShowtimeForm
def admin_required(user):
    return user.is_staff
def home(request):
    currentDate = timezone.now()
    showTimesUpNext = Showtime.objects.filter(show_time__gte=currentDate)
    movie_id_up_next = list(showTimesUpNext.values_list('movie_id', flat=True))
    movies_now_showing = Movie.objects.filter(id__in=showTimesUpNext.values('movie_id')).distinct()
    movies_hot = Movie.objects.filter(buy_count__gt=0).order_by('-buy_count')[:3]
    return render(request, 'index.html', {'movies_now_showing': movies_now_showing, "movies_hot": movies_hot, "movie_id_up_next":movie_id_up_next})
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
    cinemas = Cinema.objects.prefetch_related('showtimes__movie')

    for cinema in cinemas:
        # Lấy danh sách phim theo rạp
        cinema.movie_titles = list({s.movie.title for s in cinema.showtimes.all()})
        
        # Lấy danh sách ngày có showtime duy nhất
        cinema.show_dates = sorted({s.show_time.date() for s in cinema.showtimes.all()})
        
        # Gom showtimes theo ngày
        cinema.showtimes_by_date = {}
        for date in cinema.show_dates:
            cinema.showtimes_by_date[date] = [s for s in cinema.showtimes.all() if s.show_time.date() == date]

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
def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movie_form.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movie_form.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return redirect('movie_list')

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
