from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Movie, Cinema, Showtime, Genre


def home(request):
    current_date = timezone.now()
    showtimes_up_next = Showtime.objects.filter(show_time__gte=current_date)

    # Lấy danh sách phim sắp chiếu
    movies_now_showing = Movie.objects.filter(
        id__in=showtimes_up_next.values('movie_id')
    ).distinct()

    # Top 3 phim hot theo số lượng vé đã bán
    movies_hot = Movie.objects.filter(buy_count__gt=0).order_by('-buy_count')[:3]

    return render(request, 'index.html', {
        'movies_now_showing': movies_now_showing,
        'movies_hot': movies_hot,
        'movie_id_up_next': list(showtimes_up_next.values_list('movie_id', flat=True))
    })


def movie_list(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()

    query = request.GET.get('q')
    genre = request.GET.get('genre')

    if query:
        movies = movies.filter(title__icontains=query)
    if genre:
        # lọc theo genre name (do Genre PK = genre_name)
        movies = movies.filter(genre__genre_name=genre)

    return render(request, 'movie_list.html', {
        'movies': movies,
        'genres': genres
    })


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    now = timezone.now()
    showtimes = Showtime.objects.filter(movie=movie, show_time__gte=now).order_by("show_time")
    has_future_showtime = showtimes.exists()  
    return render(request, "movie_detail.html", {
        "movie": movie,
        "showtimes": showtimes,
        "has_future_showtime": has_future_showtime,
    })


def cinema_list(request):
    cinemas = Cinema.objects.prefetch_related('showtimes__movie')

    for cinema in cinemas:
        # Danh sách phim chiếu ở rạp
        cinema.movie_titles = list({s.movie.title for s in cinema.showtimes.all()})

        # Các ngày có lịch chiếu
        cinema.show_dates = sorted({s.show_time.date() for s in cinema.showtimes.all()})

        # Gom showtimes theo ngày
        cinema.showtimes_by_date = {}
        for date in cinema.show_dates:
            cinema.showtimes_by_date[date] = [
                s for s in cinema.showtimes.all() if s.show_time.date() == date
            ]

    return render(request, "cinema_list.html", {"cinemas": cinemas})


def cinema_detail(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    showtimes = cinema.showtimes.select_related('movie').order_by('show_time')
    return render(request, 'cinema_detail.html', {
        'cinema': cinema,
        'showtimes': showtimes
    })
