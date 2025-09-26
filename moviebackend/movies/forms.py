from django import forms
from .models import Movie, Showtime, Cinema
import os
from .utils import upload_to_supabase  # tách function upload vào utils.py để gọn


class MovieForm(forms.ModelForm):
    upload_poster = forms.ImageField(
        required=False, 
        help_text="Chọn file poster để upload"
    )
    poster_url = forms.URLField(
        required=False, 
        help_text="Hoặc nhập URL poster trực tiếp",
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Movie
        fields = ['title', 'genre', 'duration', 'description', 'release_date', 'ticket_price', 'upload_poster', 'poster_url']
        labels = {
            'title': 'Tên phim',
            'genre': 'Thể loại',
            'duration': 'Thời lượng (phút)',
            'description': 'Mô tả',
            'upload_poster': 'Ảnh poster (upload)',
            'poster_url': 'Ảnh poster (URL)',
            'release_date': 'Ngày khởi chiếu',
            'ticket_price': 'Giá vé',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ticket_price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        upload = self.cleaned_data.get("upload_poster")
        url = self.cleaned_data.get("poster_url")

        if upload:  # Nếu có upload file -> upload lên Supabase
            ext = os.path.splitext(upload.name)[1]
            fileName = f"{upload.name}{ext}"
            movieBytes = upload.read()
            url = upload_to_supabase(movieBytes, path_in_bucket=fileName, bucket_name="movies")

        if url:  # Nếu có URL hoặc vừa upload xong
            instance.poster = url

        if commit:
            instance.save()
        return instance


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
