from django.utils import timezone
from django.db.models import Sum, Count
from home.models import Posts

# Function for Updating Trending ratio


def update_trending_ratio(post, comments):
    cur_likes = post.likes.count()
    cur_views = post.views.count()
    cur_comment = comments.count()
    no_of_days_posted = abs(timezone.now().date()-post.creation_time.date()).days
    print("No of days : ", no_of_days_posted)
    if no_of_days_posted == 0:
        return
    ratio = (cur_likes * 2 + cur_views + cur_comment)/no_of_days_posted
    print("Like : ", cur_likes,
          "\nComments : ", cur_comment,
          "\nViews : ", cur_views,
          "\n days : ", no_of_days_posted,
          "\n ratio : ", ratio
          )
    post.trending_ratio = ratio
    post.save()


def update_level_by_like(post, status):
    print("Inside update level by like...")
    user_profile = post.user_profile
    likes = (
        Posts.objects
        .filter(user_profile=user_profile)  # filtering the post of specific user
        .annotate(likes_count=Count('likes'))  # counting likes on each post
        .aggregate(total_likes=Sum('likes_count'))  # Summing likes on each post to give total likes
    )
    print("I have ", likes.get('total_likes'), "Right now...")
    if likes.get('total_likes') > 25:
        return
    elif status == "increase":
        if likes.get('total_likes') == 1:
            print("Updating level by 2")
            user_profile.level += 2
        elif likes.get('total_likes') == 10:
            print("Updating level by 5")
            user_profile.level += 5
        elif likes.get('total_likes') == 25:
            print("Updating level by 10")
            user_profile.level += 10
        else:
            print("Updating level by 1")
            user_profile.level += 1
        user_profile.save()
    elif status == "decrease":
        if likes.get('total_likes') == 0:
            print("Updating level by 2")
            user_profile.level -= 2
        elif likes.get('total_likes') == 9:
            print("Updating level by 5")
            user_profile.level -= 5
        elif likes.get('total_likes') == 24:
            print("Updating level by 10")
            user_profile.level -= 10
        else:
            print("Updating level by 1")
            user_profile.level -= 1
        user_profile.save()


def update_level_by_post(all_posts, user_profile, status):
    print("Inside update level by post...")
    post_count = all_posts.filter(user_profile=user_profile).values("likes").count()
    print("User : ", user_profile, " has ", post_count, " Posts")
    print("I have ", post_count, "Right now...")
    if post_count > 20:
        return
    elif status == "increase":
        if post_count == 1:
            print("Updating level by 1")
            user_profile.level += 1
        elif post_count == 5:
            print("Updating level by 5")
            user_profile.level += 5
        elif post_count == 20:
            print("Updating level by 10")
            user_profile.level += 10
        user_profile.save()
    elif status == "decrease":
        if post_count == 0:
            print("Updating level by 1")
            user_profile.level -= 1
        elif post_count == 4:
            print("Updating level by 5")
            user_profile.level -= 5
        elif post_count == 19:
            print("Updating level by 10")
            user_profile.level -= 10
        user_profile.save()


def update_level_by_time(user_profile):
    time_with_us = abs(timezone.now().date() - user_profile.date_of_joining.date()).date()
    if time_with_us > 30:
        pass
    elif time_with_us == 30:
        user_profile.level += 5
