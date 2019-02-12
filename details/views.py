from django.shortcuts import (
    HttpResponse,
    get_object_or_404,
    reverse,
    HttpResponseRedirect
)
from django.template import loader
from .models import Posts, Comment
from signup.models import Profile
from home.data_master import update_trending_ratio
from urllib.parse import quote_plus
from django.utils import timezone
from functools import reduce
import operator
from django.db.models import Q
# Create your views here.


def details_post(request, post_id):
    print("Inside Details view")
    post = get_object_or_404(Posts, id=post_id)
    comments = Comment.objects.all().filter(post=post_id)
    if request.user.is_authenticated:
        if not (post.views.filter(id=request.user.id).exists()):
            post.views.add(request.user)                # User is Viewing the post
            update_trending_ratio(post, comments)
    share_string = quote_plus(post.title)
    trending = Posts.objects.exclude(id=post_id).order_by("-trending_ratio")
    also_like = Posts.objects.exclude(id=post_id).filter(reduce(operator.or_, (Q(tags__contains=x) for x in post.tags.split())))
    template = loader.get_template('details_post.html')
    context = {
        'post': post,
        'comments': comments,
        'share_string': share_string,
        'tags': post.tags.split(),
        'also_like': also_like,
        'trending': trending,
    }
    return HttpResponse(template.render(context, request))


def comment_submit(request, post_id):
    if request.user.is_authenticated:
        print('Inside Comment Submit')
        if request.method == 'POST':
            post = Posts.objects.get(id=post_id)
            comments = Comment.objects.all().filter(post=post)
            owner = Profile.objects.get(user=request.user)
            content = request.POST.get("comment")
            print('Content is', content)
            if post.user_profile != owner:
                if not comments.filter(user=request.user.id).exists():
                    update_trending_ratio(post, comments)
            Comment.objects.create(comment=content, post=post,
                                   user=request.user)
            print(' Comment is ', content)
            return HttpResponseRedirect(reverse('details_post',
                                        kwargs={'post_id': int(post_id)}))
    else:
        return HttpResponseRedirect(reverse('login'))
