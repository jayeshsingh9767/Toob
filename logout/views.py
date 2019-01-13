from django.shortcuts import loader, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone


def logout(request):
    template = loader.get_template('logout.html')
    print("I am Loging out... BYY", request.user.id)
    User.objects.filter(id=request.user.id).update(last_login=timezone.now())
    auth.logout(request)
    return HttpResponse(template.render({}, request))
