from django.shortcuts import loader, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone


def logout(request):
    print("I am Loging out... BYY", request.user.id)
    User.objects.filter(id=request.user.id).update(last_login=timezone.now())
    auth.logout(request)
    return render(request, 'logout.html', {})
