from django.utils import timezone
import logging
import os
from django.db.models import Sum, Count
from home.models import Posts
from Notification.notify import notify, remove_notify
from django.shortcuts import reverse

# Function for Updating Trending ratio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger(__name__)
logging.basicConfig(level=20, filename=os.path.join(BASE_DIR, 'log_file.log'))


def update_trending_ratio(post, comments):
    cur_likes = post.likes.count()
    cur_views = post.views.count()
    cur_comment = comments.count()
    no_of_days_posted = abs(timezone.now().date()-post.creation_time.date()).days
    print("No of days : ", no_of_days_posted)
    if no_of_days_posted == 0:
        post.trending_ratio = 500
        logger.info("Updated Trending ratio of " + str(post.title) + " to Maximum value")
        post.save()
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
    logger.info("Updated Trending ratio of " + str(post.title) + " to " + str(ratio))


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
            print("Increaseing level by 2")
            user_profile.level += 2
            logger.info("Increaseing Level of " + str(user_profile.user) + " by 2")
            notify(user_profile, user_profile, "Your Level is Updated By 2", 40, reverse('home'))
        elif likes.get('total_likes') == 10:
            print("Increaseing level by 5")
            user_profile.level += 5
            logger.info("Increaseing Level of " + str(user_profile.user) + " by 5")
            notify(user_profile, user_profile, "Your Level is Updated By 5", 40, reverse('home'))
        elif likes.get('total_likes') == 25:
            print("Increaseing level by 10")
            user_profile.level += 10
            logger.info("Increaseing Level of " + str(user_profile.user) + " by 10")
            notify(user_profile, user_profile, "Your Level is Updated By 10", 40, reverse('home'))
        elif likes.get('total_likes') % 10 == 0:
            print("Increaseing level by 1")
            user_profile.level += 1
            logger.info("Increaseing Level of " + str(user_profile.user) + " by 1")
            notify(user_profile, user_profile, "Your Level is Updated By 1", 40, reverse('home'))
        user_profile.save()
    elif status == "decrease":
        if likes.get('total_likes') == 0:
            print("Decreaseing level by 2")
            user_profile.level -= 2
            logger.info("Decreaseing Level of " + str(user_profile.user) + " by 2")
            remove_notify(user_profile, user_profile, "Your Level is Updated By 2", 40, reverse('home'))
        elif likes.get('total_likes') == 9:
            print("Decreaseing level by 5")
            user_profile.level -= 5
            logger.info("Decreaseing Level of " + str(user_profile.user) + " by 5")
            remove_notify(user_profile, user_profile, "Your Level is Updated By 5", 40, reverse('home'))
        elif likes.get('total_likes') == 24:
            print("Decreaseing level by 10")
            user_profile.level -= 10
            logger.info("Decreaseing Level of " + str(user_profile.user) + " by 10")
            remove_notify(user_profile, user_profile, "Your Level is Updated By 10", 40, reverse('home'))
        elif likes.get('total_likes') % 9 == 0:
            print("Decreaseing level by 1")
            user_profile.level -= 1
            logger.info("Decreaseing Level of " + str(user_profile.user) + " by 1")
            remove_notify(user_profile, user_profile, "Your Level is Updated By 1", 40, reverse('home'))
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
            print("Increaseing level by 1")
            user_profile.level += 1
            logger.info("Increaseing Level of " + str(user_profile.user) + " by 1")
            notify(user_profile, user_profile, "Your Level is Updated By 1", 40, reverse('home'))
        elif post_count == 5:
            print("Increaseing level by 5")
            user_profile.level += 5
            logger.info("Increaseing Level of " + str(user_profile.user) + " by 5")
            notify(user_profile, user_profile, "Your Level is Updated By 5", 40, reverse('home'))
        elif post_count == 20:
            print("Increaseing level by 10")
            user_profile.level += 10
            logger.info("Increaseing Level of " + str(user_profile.user) + " by 10")
            notify(user_profile, user_profile, "Your Level is Updated By 10", 40, reverse('home'))
        user_profile.save()
    elif status == "decrease":
        if post_count == 0:
            print("Decreaseing level by 1")
            user_profile.level -= 1
            logger.info("Decreaseing Level of " + str(user_profile.user) + " by 1")
        elif post_count == 4:
            print("Decreaseing level by 5")
            logger.info("Decreaseing Level of " + str(user_profile.user) + " by 2")
            user_profile.level -= 5
        elif post_count == 19:
            print("Decreaseing level by 10")
            user_profile.level -= 10
            logger.info("Decreaseing Level of " + str(user_profile.user) + " by 10")
        user_profile.save()


def update_level_by_time(user_profile):
    time_with_us = abs(timezone.now().date() - user_profile.date_of_joining.date()).date()
    if time_with_us == 30:
        user_profile.level += 5
