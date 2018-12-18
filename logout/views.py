from django.shortcuts import render, loader, HttpResponse
from django.contrib import auth


def logout(request):
    template = loader.get_template('logout.html')
    auth.logout(request)
    print("I am Loging out... BYY")
    return HttpResponse(template.render({}, request))
