from django.shortcuts import reverse, HttpResponseRedirect
from django.shortcuts import render
from signup.models import Profile

# Create your views here.


def explore(request):
    if request.user.is_authenticated:
        all_user = Profile.objects.all().exclude(user=request.user).order_by('-level')
        logged_in_user_profile = Profile.objects.get(user=request.user)
        followings = Profile.objects.filter(user=request.user).values('follows')
        followers = Profile.objects.filter(follows=logged_in_user_profile)
        context = {
            'all_user': all_user,
            'logged_in_user_profile': logged_in_user_profile,
            'followings': followings,
            'followers': followers,
        }
        return render(request, 'explore.html', context)
    else:
        return HttpResponseRedirect(reverse("login"))
