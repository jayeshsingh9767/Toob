from django.shortcuts import render, loader, HttpResponse
# Create your views here.


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render({}, request))
