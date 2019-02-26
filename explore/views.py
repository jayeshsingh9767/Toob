from django.shortcuts import render
from signup.models import Profile

# Create your views here.


def explore(request):
    if request.user.is_authenticated:
        all_user = Profile.objects.all().exclude(user=request.user).order_by('-level')
        logged_in_user_profile = Profile.objects.get(user=request.user)
        context = {
            'all_user': all_user,
            'logged_in_user_profile': logged_in_user_profile,
        }
        return render(request, 'explore.html', context)
    else:
        all_user = Profile.objects.all().order_by('-level')
        return render(request, 'explore.html', {"all_user": all_user})


def followers(request):
    if request.user.is_authenticated:
        logged_in_user_profile = Profile.objects.get(user=request.user)
        followers = Profile.objects.filter(follows=logged_in_user_profile)
        context = {
            'logged_in_user_profile': logged_in_user_profile,
            'followers': followers,
        }
        return render(request, 'followers.html', context)
    else:
        return render(request, 'followers.html', {})


def followings(request):
    if request.user.is_authenticated:
        logged_in_user_profile = Profile.objects.get(user=request.user)
        followings = Profile.objects.get(id=logged_in_user_profile.id).follows.all()
        context = {
            'logged_in_user_profile': logged_in_user_profile,
            'followings': followings,
        }
        return render(request, 'followings.html', context)
    else:
        return render(request, 'followings.html', {})
