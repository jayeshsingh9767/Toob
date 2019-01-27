from django.utils import timezone

# Function for Updating Trending ratio


def update_trending_ratio(post, comments):
    cur_likes = post.likes.count()
    cur_views = post.views.count()
    cur_comment = comments.count()
    no_of_days_posted = abs(timezone.now().date()-post.creation_time.date()).days
    ratio = (cur_likes * 2 + cur_views + cur_comment)/no_of_days_posted
    print("Like : ", cur_likes,
          "\nComments : ", cur_comment,
          "\nViews : ", cur_views,
          "\n days : ", no_of_days_posted,
          "\n ratio : ", ratio
          )
    post.trending_ratio = ratio
    post.save()


def update_level_by_like(all_posts, user_profile):
    like_count = all_posts.filter(user_profile=user_profile).values('likes').count()
    if like_count > 25:
        pass
    elif like_count == 1:
        user_profile.level += 2
    elif like_count == 10:
        user_profile.level += 5
    elif like_count == 25:
        user_profile.level += 10
    else:
        user_profile.level += 1


def update_level_by_post(all_posts, user_profile):
    post_count = all_posts.filter(user_profile=user_profile).count()
    if post_count > 20:
        pass
    elif post_count == 1:
        user_profile.level += 1
    elif post_count == 5:
        user_profile.level += 5
    elif post_count == 20:
        user_profile.level += 10


def update_level_by_time(user_profile):
    time_with_us = abs(timezone.now().date() - user_profile.date_of_joining.date()).date()
    if time_with_us > 30:
        pass
    elif time_with_us == 30:
        user_profile.level += 5
