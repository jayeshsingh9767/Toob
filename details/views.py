from django.shortcuts import HttpResponse, get_object_or_404, reverse, HttpResponseRedirect
from django.template import loader
from .models import Posts, Comment
# Create your views here.


def details_post(request, post_id):
    print("Inside Details view")
    post = get_object_or_404(Posts, id=post_id)
    comments = Comment.objects.all().filter(post=post_id)
    template = loader.get_template('details_post.html')
    context = {
        'post': post,
        'comments': comments,
    }
    return HttpResponse(template.render(context, request))


def comment_submit(request, post_id):
    if request.method == 'POST':
        post = Posts.objects.get(id=post_id)
        content = request.POST.get("comment")
        Comment.objects.create(comment=content, post=post,
                               user=request.user)
        print(' Comment is ', content)
        return HttpResponseRedirect(reverse('details_post', args=post_id))
