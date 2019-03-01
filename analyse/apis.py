from django.http import JsonResponse
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from signup.models import Profile
from home.models import Posts


def get_trend_user_api(request):
    if request.user.is_superuser:
        jan = User.objects.filter(date_joined__month=1).count()
        feb = User.objects.filter(date_joined__month=2).count()+jan
        mar = User.objects.filter(date_joined__month=3).count()+feb
        apr = User.objects.filter(date_joined__month=4).count()+mar
        may = User.objects.filter(date_joined__month=5).count()+apr
        june = User.objects.filter(date_joined__month=6).count()+may
        july = User.objects.filter(date_joined__month=7).count()+june
        aug = User.objects.filter(date_joined__month=8).count()+july
        sep = User.objects.filter(date_joined__month=9).count()+aug
        oct = User.objects.filter(date_joined__month=10).count()+sep
        nov = User.objects.filter(date_joined__month=11).count()+oct
        dec = User.objects.filter(date_joined__month=12).count()+nov
        data_set = [jan, feb, mar, apr, may, june, july, aug, sep, oct, nov, dec]
        data = {
            'data_set': data_set
        }
        return JsonResponse(data)


def get_popular_user(request):
    if request.user.is_superuser:
        top_10 = Profile.objects.order_by('-level')[:10]
        user_labels = []
        user_level = []
        followers = []
        followings = []
        for i in top_10:
            user_labels.append(i.user.first_name)
            user_level.append(i.level)
            follg = Profile.objects.all().filter(follows=i.id).count()
            followers.append(follg)
            follr = Profile.objects.get(id=i.id)
            followings.append(follr.follows.count())
        data = {
            'user_labels': user_labels,
            'user_level': user_level,
            'followers': followers,
            'followings': followings
        }
        return JsonResponse(data)


def get_user_api(request, user_id):
    if request.user.is_superuser:
        user = Profile.objects.get(id=user_id)
        level = user.level
        followers = Profile.objects.all().filter(follows=user).count()
        likes = (
            Posts.objects
            .filter(user_profile=user_id)  # filtering the post of specific user
            .annotate(likes_count=Count('likes'))  # counting likes on each post
            .aggregate(total_likes=Sum('likes_count'))  # Summing likes on each post to give total likes
        )
        followings = user.follows.count()
        post = Posts.objects.filter(user_profile=user).count()

        parameters = [level, followers, likes.get('total_likes'), followings, post]
        print("Data is : ", parameters)
        data = {"parameters": parameters}
        return JsonResponse(data)
