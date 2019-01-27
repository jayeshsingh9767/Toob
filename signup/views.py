from django.shortcuts import (
    render,
    get_object_or_404,
    HttpResponseRedirect,
    reverse
)
from django.contrib.auth.forms import authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from signup.forms import UserSignUp
from home.models import Posts
from . models import Profile
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User


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


def profile(request, user_id):   # when profile page is called
    print("Inside Profile page...")
    user_profile = get_object_or_404(Profile, id=user_id)
    logged_in_user_profile = get_object_or_404(Profile,
                                               user=request.user.id)
    user_post = Posts.objects.all().filter(user_profile=user_id).order_by("-trending_ratio")
    following = Profile.objects.all().filter(follows=user_profile.id)
    like_count = Posts.objects.all().filter(user_profile=user_profile).values('likes').count()
    context = {
        'logged_in_user_profile': logged_in_user_profile,
        'user_profile': user_profile,
        'user_post': user_post,
        'following': following,
        'like_count': like_count
    }
    return render(request, 'profile.html', context)


def follow(request):      # calls when any user follows other user
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
            logged_in_user_profile.level -= 2
        else:
            print("Not folloed")
            logged_in_user_profile.follows.add(user_profile)
            logged_in_user_profile.level += 2
        context = {
            'user_profile': user_profile,
            'logged_in_user_profile': logged_in_user_profile,
        }
    if request.is_ajax():
        follow_button = render_to_string('follow_section.html',
                                         context, request=request)
        return JsonResponse({'follow_button': follow_button})


def edit_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'edit_profile.html', context)


def edit_submit(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        profile_pic = request.FILES.get('profile_pic')
        bio = request.POST.get('bio')
        email = request.POST.get('email-id')
        city = request.POST.get('city')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        print('User is:', request.user.id)
        # user_obj = User.objects.get(id=request.user.id)
        # user_obj.username = username
        print('Profile img is :', profile_pic)
        user_profile = Profile.objects.get(user=request.user)
        if profile_pic is not None:
            user_profile.profile_pic = profile_pic
            user_profile.save()
        User.objects.filter(id=request.user.id).update(
            username=username, first_name=firstname, last_name=lastname,
            email=email,
        )
        p = Profile.objects.filter(user=request.user.id).update(
            bio=bio,
            city=city,
            date_of_birth=dob,
            gender=gender
        )
        print(" Number of rows modifid is :", p)
        return HttpResponseRedirect(reverse('profile', args=[user_profile.id]))
