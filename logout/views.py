from django.shortcuts import render
import os
import logging
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger(__name__)
logging.basicConfig(level=20, filename=os.path.join(BASE_DIR, 'log_file.log'))


def logout(request):
    print("I am Loging out... BYY", request.user.id)
    User.objects.filter(id=request.user.id).update(last_login=timezone.now())
    logger.critical(str(request.user) + " is Logging out from the Site")
    auth.logout(request)
    return render(request, 'logout.html', {})
