from django import forms
from .models import Movie, Showtime, Cinema


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'duration', 'description', 'poster', 'release_date', 'ticket_price']
        labels = {
            'title': 'Tên phim',
            'genre': 'Thể loại',
            'duration': 'Thời lượng (phút)',
            'description': 'Mô tả',
            'poster': 'Ảnh poster',
            'release_date': 'Ngày khởi chiếu',
            'ticket_price': 'Giá vé',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'poster': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ticket_price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class ShowtimeForm(forms.ModelForm):
    class Meta:
        model = Showtime
        fields = ['movie', 'cinema', 'show_time']
        labels = {
            'movie': 'Phim',
            'cinema': 'Rạp',
            'show_time': 'Thời gian chiếu',
        }
        widgets = {
            'movie': forms.Select(attrs={'class': 'form-control'}),
            'cinema': forms.Select(attrs={'class': 'form-control'}),
            'show_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }


class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ['name', 'location']
        labels = {
            'name': 'Tên rạp',
            'location': 'Địa điểm',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
