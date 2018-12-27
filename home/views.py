from django.shortcuts import loader, HttpResponse, get_object_or_404, HttpResponseRedirect
from .models import Posts
from django.template.loader import render_to_string
from signup.models import Profile


def home(request):
    template = loader.get_template('home.html')
    all_posts = Posts.objects.all()
    context = {
        'all_posts': all_posts,
    }
    return HttpResponse(template.render(context, request))


def like_post(request):
    print("Insisde Like Post")
    post = get_object_or_404(Posts, id=request.POST.get('id'))  # for AJAX call
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)                 # Liking The Post
        print("DisLiking the post")
    else:
        post.likes.add(request.user)
        print("Liking the post")
    if request.is_ajax():
        html = render_to_string('')

    return HttpResponseRedirect('/')
