from django.shortcuts import (
    loader,
    get_object_or_404,
    render,
    HttpResponseRedirect,
    reverse,
    HttpResponse
)
import logging
import os
from .models import Posts
from details.models import Comment
from django.template.loader import render_to_string
from django.http import JsonResponse
from signup.models import Profile
from .forms import WriteThought
from Notification.notify import notify, remove_notify
from home.data_master import (
    update_trending_ratio,
    update_level_by_like,
    update_level_by_post
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger(__name__)
logging.basicConfig(level=20, filename=os.path.join(BASE_DIR, 'log_file.log'))


def home(request):
    popular = Profile.objects.order_by('-level')
    if request.user.is_authenticated:
        logged_user = Profile.objects.get(user=request.user.id)
        followings = logged_user.follows.all()
        all_posts = Posts.objects.filter(user_profile__in=followings).order_by('-trending_ratio')
        print('Logged user : ', logged_user.id)
        context = {
            'all_posts': all_posts,
            'logged_user': logged_user,
            'followings': followings,
            'popular': popular,
        }
        return render(request, 'home.html', context)
    else:
        all_posts = Posts.objects.order_by('-trending_ratio')
        context = {
            'all_posts': all_posts,
            'popular': popular
        }
        return render(request, 'home.html', context)


def write_thought(request):
    if request.user.is_authenticated:
        form = WriteThought(initial={'type': '5'})
        return render(request, 'write_thought.html', {'form': form})
    else:
        logger.critical(" Unauthenticated user tries to access the secured URL ")
        return HttpResponseRedirect(reverse('login'))


def post_thought(request):
    if request.user.is_authenticated:
        if request.POST:
            # print("Post is Submiting")
            user_profile = Profile.objects.get(user=request.user.id)
            title = request.POST.get("title")
            content = request.POST.get("content")
            type = request.POST.get("type")
            img = request.FILES.get("image")
            tags = request.POST.get("tags")
            print("Image data is : ", img)
            pos = Posts.objects.filter(title=title)
            if pos:
                print("Post already Exixts")
                return HttpResponse(
                    "<center><h3>Post with title '" + title + "' already Exixts</h3><br><Try another Title></center>"
                )
            Posts.objects.create(
                title=title,
                content=content,
                type=type,
                image=img,
                tags=tags,
                user_profile=user_profile
            )
            logger.info(str(request.user) + " Writes a Thought : " + str(title))
            all_posts = Posts.objects.all()
            update_level_by_post(all_posts, user_profile, 'increase')
            return HttpResponseRedirect(reverse('home'))
        else:
            logger.critical(" Unauthenticated user tries to access the secured URL ")
            return HttpResponseRedirect(reverse('login'))


def like_post(request):
    if request.user.is_authenticated:
        all_posts = Posts.objects.all()
        print("Insisde Like Post")
        print('ID coming from form is', request.POST.get('id'))
        post = get_object_or_404(Posts, id=request.POST.get('id'))  # for AJAX call
        user_profile = Profile.objects.get(user=request.user)
        comments = Comment.objects.all().filter(post=post)
        context = {
            'all_posts': all_posts,
            'post': post
        }
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)                # Disliking The Post
            logger.info(str(request.user) + " Removed like from Thought : " + str(post.title))
            remove_notify(user_profile, post.user_profile, "Liked Your Post", 30, reverse('details_post', args=[post.id]))
            update_trending_ratio(post, comments)
            update_level_by_like(post, "decrease")
            # print("DisLiking the post")
        else:
            post.likes.add(request.user)
            logger.info(str(request.user) + " Liked a Thought : " + str(post.title))
            notify(user_profile, post.user_profile, "Liked Your Post", 30, reverse('details_post', args=[post.id]))
            update_trending_ratio(post, comments)
            update_level_by_like(post, "increase")
            post.dis_likes.remove(request.user)
            # print("Liking the post")
        if request.is_ajax():
            print('Hey its an AJAX calls')    # TEsting AJAX request
            html = render_to_string('like_section.html', context, request=request)
            html2 = render_to_string('dis_like_section.html',
                                     context, request=request)
            return JsonResponse({'like_form': html, 'dis_like_form': html2})
    else:
        logger.critical(" Unauthenticated user tries to access the secured URL ")
        return HttpResponseRedirect(reverse('login'))


def dis_like_post(request):
    if request.user.is_authenticated:
        all_posts = Posts.objects.all()
        print("Insisde Dis Like Post")
        print('ID coming from form is', request.POST.get('id'))
        user_profile = Profile.objects.get(user=request.user)  # looged in user
        post = get_object_or_404(Posts, id=request.POST.get('id'))  # for AJAX call
        context = {
            'all_posts': all_posts,
            'post': post
        }
        if post.dis_likes.filter(id=request.user.id).exists():
            post.dis_likes.remove(request.user)               # Liking The Post
            logger.info(str(request.user) + " Removed Dislike from Thought : " + str(post.title))
            remove_notify(user_profile, post.user_profile, "Disliked Your Post", 30, reverse('details_post', args=[post.id]))
            update_level_by_like(post, "decrease")
            # print("removing dislike ")
        else:
            post.dis_likes.add(request.user)
            logger.info(str(request.user) + " Disliked a Thought : " + str(post.title))
            notify(user_profile, post.user_profile, "Disliked Your Post", 30, reverse('details_post', args=[post.id]))
            post.likes.remove(request.user)
            update_level_by_like(post, "decrease")
            # print("Adding Dislike")
        if request.is_ajax():
            print('Hey its an AJAX calls')          # TEsting AJAX request
            html = render_to_string('dis_like_section.html', context,
                                    request=request)
            html2 = render_to_string('like_section.html', context,
                                     request=request)
            return JsonResponse({'dis_like_form': html, 'like_form': html2})
    else:
        logger.critical(" Unauthenticated user tries to access the secured URL ")
        return HttpResponseRedirect(reverse('login'))


def temp(request):
    print("that must be logged")
    logger.error("It is Test Error For Logging modeule")
