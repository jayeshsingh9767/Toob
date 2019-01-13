from django.utils import timezone

# Function for Updating Trending ratio


def update_trending_ratio(post, comments, operataion):
    cur_likes = post.likes.count()
    cur_views = post.views.count()
    cur_comment = comments.count()
    no_of_days_posted = abs(timezone.now().date()-post.creation_time.date()).days
    ratio = (cur_likes * 2 + cur_views + cur_comment)/no_of_days_posted
    print("Like : ", cur_likes,
          "\nComments : ", cur_comment,
          "\nViews : ", cur_views,
          "\n days : ", no_of_days_posted,
          "\n ration : ", ratio
          )
    if operataion == "+":
        post.trending_ratio += ratio
        post.save()
    if operataion == "-":
        post.trending_ratio -= ratio
        post.save()
