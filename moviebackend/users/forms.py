from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from movies.models import Cinema
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('M', 'Nam'), ('F', 'Nữ')], required=False)
    favorite_cinema = forms.ModelChoiceField(
        queryset=None,  
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'address',
            'birth_date', 'gender', 'favorite_cinema',
            'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from movies.models import Cinema
        self.fields['favorite_cinema'].queryset = Cinema.objects.all()



class UserUpdateForm(UserChangeForm):
    password = None  

    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(max_length=15, required=False, label="Số điện thoại")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Địa chỉ")
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Ngày sinh"
    )
    gender = forms.ChoiceField(
        choices=[('', '--- Chọn ---'), ('M', 'Nam'), ('F', 'Nữ')],
        required=False,
        label="Giới tính"
    )
    favorite_cinema = forms.ModelChoiceField(
        queryset=Cinema.objects.all(),
        required=False,
        label="Rạp yêu thích"
    )
    upload_avatar = forms.ImageField(required=False, label="Ảnh đại diện")
    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'address',
            'birth_date', 'gender', 'favorite_cinema', 'avatar'
        ]