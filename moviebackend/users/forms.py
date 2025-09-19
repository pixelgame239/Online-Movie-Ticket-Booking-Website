# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from movies.models import Region, Cinema

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False, label="Ngày sinh"
    )
    gender = forms.ChoiceField(
        choices=[('M', 'Nam'), ('F', 'Nữ')],
        widget=forms.RadioSelect,
        required=False, label="Giới tính"
    )
    region = forms.ModelChoiceField(queryset=Region.objects.none(), required=False, label="Khu vực")
    favorite_cinema = forms.ModelChoiceField(queryset=Cinema.objects.none(), required=False, label="Rạp yêu thích")

    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'address',
            'birth_date', 'gender', 'region', 'favorite_cinema',
            'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].queryset = Region.objects.all()
        self.fields['favorite_cinema'].queryset = Cinema.objects.all()

class UserUpdateForm(UserChangeForm):
    password = None  
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False, label="Ngày sinh"
    )
    gender = forms.ChoiceField(
        choices=[('M', 'Nam'), ('F', 'Nữ')],
        widget=forms.RadioSelect,
        required=False, label="Giới tính"
    )
    region = forms.ModelChoiceField(queryset=Region.objects.none(), required=False, label="Khu vực")
    favorite_cinema = forms.ModelChoiceField(queryset=Cinema.objects.none(), required=False, label="Rạp yêu thích")

    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'address',
            'birth_date', 'gender', 'region', 'favorite_cinema'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].queryset = Region.objects.all()
        self.fields['favorite_cinema'].queryset = Cinema.objects.all()

