from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from signup.models import Profile
from wsgiref.util import FileWrapper
import os
from django.conf import settings

# Create your views here.


def analyse(request):
    if request.user.is_superuser:
        return render(request, 'analyse.html', {})
    else:
        return HttpResponseRedirect('/admin/login/?next=/admin/')


def user_level(request):
    if request.user.is_superuser:
        return render(request, 'analyse_user_level.html', {})
    else:
        return HttpResponseRedirect('/admin/login/?next=/admin/')


def toob_growth(request):
    if request.user.is_superuser:
        return render(request, 'toob_growth.html', {})
    else:
        return HttpResponseRedirect('/admin/login/?next=/admin/')


def select_user(request):
    if request.user.is_superuser:
        user_list = Profile.objects.all()
        return render(request, 'select_user.html', {"user_list": user_list})
    else:
        return HttpResponseRedirect('/admin/login/?next=/admin/')


def analyse_user(request, user_id):
    if request.user.is_superuser:
        user = Profile.objects.get(id=user_id)
        return render(request, 'analyse_user.html', {"user": user})
    else:
        return HttpResponseRedirect('/admin/login/?next=/admin/')


def compare_user(request):
    if request.user.is_superuser:
        if request.POST:
            user1 = request.POST.get('firstUser')
            user2 = request.POST.get('secondUser')
            firstUser = Profile.objects.get(id=user1)
            secondUser = Profile.objects.get(id=user2)
            context = {
                'firstUser': firstUser,
                'secondUser': secondUser
            }
            return render(request, 'compare_user.html', context)


def analyse_post(request):
    if request.user.is_superuser:
        return render(request, 'analyse_post.html', {})
    else:
        return HttpResponseRedirect('/admin/login/?next=/admin/')


def tags(request):
    if request.user.is_superuser:
        return render(request, 'tag_analysis.html', {})
    else:
        return HttpResponseRedirect('/admin/login/?next=/admin/')


def log_file(request):
    if request.user.is_superuser:
        filename = os.path.join(settings.BASE_DIR, 'log_file.log')
        if os.path.exists(filename):
            with open(filename, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/plain")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
                return response
    else:
        return HttpResponseRedirect('/admin/login/?next=/admin/')
    
