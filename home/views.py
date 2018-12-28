from django.shortcuts import loader, HttpResponse, get_object_or_404, HttpResponseRedirect
from .models import Posts
from django.template.loader import render_to_string
from django.http import JsonResponse
from signup.models import Profile


def home(request):
    template = loader.get_template('home.html')
    all_posts = Posts.objects.all()
    context = {
        'all_posts': all_posts,
    }
    return HttpResponse(template.render(context, request))


def like_post(request):
    all_posts = Posts.objects.all()
    print("Insisde Like Post")
    print('ID coming from form is', request.POST.get('id'))
    post = get_object_or_404(Posts, id=request.POST.get('id'))  # for AJAX call
    context = {
        'all_posts': all_posts,
        'post': post
    }
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)                 # Liking The Post
        print("DisLiking the post")
    else:
        post.likes.add(request.user)
        print("Liking the post")
    if request.is_ajax():
        print('Hey its an AJAX calls')    # TEsting AJAX request
        html = render_to_string('like_section.html', context, request=request)
        return JsonResponse({'form': html})
