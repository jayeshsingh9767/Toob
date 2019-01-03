from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib.auth.forms import UserCreationForm, authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from signup.forms import UserSignUp
from home.models import Posts
from . models import Profile
from django.http import JsonResponse
from django.template.loader import render_to_string


def get_followers(user_profile):
    all_user = Profile.objects.all().filter(follows=user_profile.id)
    following = 0
    for i in all_user:
        following = following + 1
    return following


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


def profile(request, user_id):
    print("Inside Profile page...")
    user_profile = get_object_or_404(Profile, id=user_id)
    logged_in_user_profile = get_object_or_404(Profile,
                                               user=request.user.id)
    user_post = Posts.objects.all().filter(user_profile=user_id)
    following = get_followers(user_profile)
    context = {
        'logged_in_user_profile': logged_in_user_profile,
        'user_profile': user_profile,
        'user_post': user_post,
        'following': following
    }
    return render(request, 'profile.html', context)


def follow(request):
    print("Followings user...")
    if request.POST:
        user_id = request.POST.get('id')
        user_profile = get_object_or_404(Profile, user=user_id)
        logged_in_user_profile = get_object_or_404(Profile,
                                                   user=request.user.id)
        print("This page belongs to ", user_profile)
        print("Loged in User is ", logged_in_user_profile)
        if logged_in_user_profile.follows.filter(id=user_profile.id).exists():
            print("Already followed")
            logged_in_user_profile.follows.remove(user_profile)
        else:
            print("Not folloed")
            logged_in_user_profile.follows.add(user_profile)
        context = {
            'user_profile': user_profile,
            'logged_in_user_profile': logged_in_user_profile,
        }
    if request.is_ajax():
        follow_button = render_to_string('follow_section.html',
                                         context, request=request)
        return JsonResponse({'follow_button': follow_button})
