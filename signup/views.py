from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from signup.forms import UserSignUp


def signup(request):
    if request.method == 'POST':
        form = UserSignUp(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.gender = form.cleaned_data.get('gender')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserSignUp()
    return render(request, 'signup.html', {'form': form})
