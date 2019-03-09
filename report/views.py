from django.shortcuts import HttpResponse, HttpResponseRedirect, reverse
from .models import Report
from signup.models import Profile
from home.models import Posts
import os
import logging
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger(__name__)
logging.basicConfig(level=20, filename=os.path.join(BASE_DIR, 'log_file.log'))


def report_post(request, post_id):
    if request.method == "POST":
        logged_user = Profile.objects.get(user=request.user)
        post = Posts.objects.get(id=post_id)
        if not (Report.objects.filter(post=post, user=logged_user).exists()):
            reason = request.POST.get('reason')
            other = ''
            if reason == '5':
                other = request.POST.get('other')
            re = Report(post=post, user=logged_user, reporting_reason=reason, other_reason=other)
            re.save()
            print("Its There")
            logger.info(str(logged_user.user.username) + " Reported The Thought " + str(post.title))
        return HttpResponseRedirect(reverse('details_post', kwargs={'post_id': post_id}))
