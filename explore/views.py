from django.shortcuts import reverse, HttpResponseRedirect
from django.shortcuts import render
from signup.models import Profile

# Create your views here.


def explore(request):
    all_user = Profile.objects.all().exclude(user=request.user).order_by('-level')
    logged_in_user_profile = Profile.objects.get(user=request.user)
    context = {
        'all_user': all_user,
        'logged_in_user_profile': logged_in_user_profile,
    }
    return render(request, 'explore.html', context)


def followers(request):
    logged_in_user_profile = Profile.objects.get(user=request.user)
    followers = Profile.objects.filter(follows=logged_in_user_profile)
    context = {
        'logged_in_user_profile': logged_in_user_profile,
        'followers': followers,
    }
    return render(request, 'followers.html', context)


def followings(request):
    logged_in_user_profile = Profile.objects.get(user=request.user)
    followings = Profile.objects.get(id=2).follows.all()
    context = {
        'logged_in_user_profile': logged_in_user_profile,
        'followings': followings,
    }
    return render(request, 'followings.html', context)
