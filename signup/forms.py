from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserSignUp(UserCreationForm):
    CHOICES = [('male', 'Male'), ('female', 'Female')]
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email ID'}))
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget(years=range(1970, 2018)))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City'}))
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password confirm'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'city', 'gender', 'password1', 'password2')

