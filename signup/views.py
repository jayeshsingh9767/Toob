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
from django.db.models import Sum, Count
from Notification.notify import notify, remove_notify


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
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, id=user_id)
        logged_in_user_profile = get_object_or_404(Profile,
                                                   user=request.user.id)
        user_post = Posts.objects.all().filter(user_profile=user_id).order_by("-trending_ratio")
        following = Profile.objects.all().filter(follows=user_profile.id)
        likes = (
            Posts.objects
            .filter(user_profile=user_id)  # filtering the post of specific user
            .annotate(likes_count=Count('likes'))  # counting likes on each post
            .aggregate(total_likes=Sum('likes_count'))  # Summing likes on each post to give total likes
        )
        context = {
            'logged_in_user_profile': logged_in_user_profile,
            'user_profile': user_profile,
            'user_post': user_post,
            'following': following,
            'total_likes': likes.get('total_likes')
        }

        return render(request, 'profile.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def follow(request):      # called when any user follows other user
    if request.user.is_authenticated:
        print("Followings user...")
        if request.POST:
            user_id = request.POST.get('id')
            print("user id is :", user_id)
            user_profile = get_object_or_404(Profile, user=user_id)
            print("check 2")
            logged_in_user_profile = get_object_or_404(Profile,
                                                       user=request.user.id)
            print("This page belongs to ", user_profile)
            print("Loged in User is ", logged_in_user_profile)
            if logged_in_user_profile.follows.filter(id=user_profile.id).exists():
                print("Already followed")
                logged_in_user_profile.follows.remove(user_profile)
                remove_notify(logged_in_user_profile, user_profile, "Started Following You", 30, reverse('profile', args=[logged_in_user_profile.id]))
            else:
                print("Not folloed")
                logged_in_user_profile.follows.add(user_profile)
                notify(logged_in_user_profile, user_profile, "Started Following You", 30, reverse('profile', args=[logged_in_user_profile.id]))
            context = {
                'user_profile': user_profile,
                'logged_in_user_profile': logged_in_user_profile,
            }
            print("End of Post request")
        if request.is_ajax():
            follow_button = render_to_string('follow_section.html',
                                             context, request=request)
            return JsonResponse({'follow_button': follow_button})
    else:
        return HttpResponseRedirect(reverse('login'))


def edit_profile(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        context = {
            'user_profile': user_profile
        }
        return render(request, 'edit_profile.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def edit_submit(request):
    if request.user.is_authenticated:
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
        else:
            return HttpResponseRedirect(reverse('login'))
