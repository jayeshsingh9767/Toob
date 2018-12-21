from django.shortcuts import render, loader, HttpResponse
from .models import Posts, Upvote, Down_vote


def home(request):
    template = loader.get_template('home.html')
    all_posts = Posts.objects.all()
    context = {
        'all_posts': all_posts
    }
    return HttpResponse(template.render(context, request))
