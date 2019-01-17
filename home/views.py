from django.shortcuts import (
    loader,
    HttpResponse,
    get_object_or_404,
    render,
    HttpResponseRedirect,
    reverse
)
from .models import Posts
from details.models import Comment
from django.template.loader import render_to_string
from django.http import JsonResponse
from signup.models import Profile
from .forms import WriteThought
from home.data_master import update_trending_ratio


def home(request):
    if request.user.is_authenticated:
        template = loader.get_template('home.html')
        logged_user = Profile.objects.get(user=request.user.id)
        followings = logged_user.follows.all()
        all_posts = []
        for foll in followings:
            all_posts += Posts.objects.all().filter(user_profile=foll.id)
        # all_posts.reverse()
        print('Logged user : ', logged_user.id)
        context = {
            'all_posts': all_posts,
            'logged_user': logged_user,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect(reverse("login"))


def write_thought(request):
    form = WriteThought(initial={'type': '5'})
    return render(request, 'write_thought.html', {'form': form})


def post_thought(request):
    if request.POST:
        print("Post is Submiting")
        user_profile = Profile.objects.get(user=request.user.id)
        title = request.POST.get("title")
        content = request.POST.get("content")
        type = request.POST.get("type")
        img = request.FILES.get("image")
        tags = request.POST.get("tags")
        print("Image data is : ", img)
        Posts.objects.create(
            title=title,
            content=content,
            type=type,
            image=img,
            tags=tags,
            user_profile=user_profile
        )
        return HttpResponseRedirect(reverse('home'))


def like_post(request):
    all_posts = Posts.objects.all()
    print("Insisde Like Post")
    print('ID coming from form is', request.POST.get('id'))
    post = get_object_or_404(Posts, id=request.POST.get('id'))  # for AJAX call
    comments = Comment.objects.all().filter(post=post)
    context = {
        'all_posts': all_posts,
        'post': post
    }
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)                 # Liking The Post
        update_trending_ratio(post, comments)
        print("DisLiking the post")
    else:
        post.likes.add(request.user)
        update_trending_ratio(post, comments)
        post.dis_likes.remove(request.user)
        print("Liking the post")
    if request.is_ajax():
        print('Hey its an AJAX calls')    # TEsting AJAX request
        html = render_to_string('like_section.html', context, request=request)
        html2 = render_to_string('dis_like_section.html',
                                 context, request=request)
        return JsonResponse({'like_form': html, 'dis_like_form': html2})


def dis_like_post(request):
    all_posts = Posts.objects.all()
    print("Insisde Dis Like Post")
    print('ID coming from form is', request.POST.get('id'))
    post = get_object_or_404(Posts, id=request.POST.get('id'))  # for AJAX call
    context = {
        'all_posts': all_posts,
        'post': post
    }
    if post.dis_likes.filter(id=request.user.id).exists():
        post.dis_likes.remove(request.user)                 # Liking The Post
        print("removing dislike ")
    else:
        post.dis_likes.add(request.user)
        post.likes.remove(request.user)
        print("Adding Dislike")
    if request.is_ajax():
        print('Hey its an AJAX calls')          # TEsting AJAX request
        html = render_to_string('dis_like_section.html', context,
                                request=request)
        html2 = render_to_string('like_section.html', context,
                                 request=request)
        return JsonResponse({'dis_like_form': html, 'like_form': html2})
