from django.shortcuts import render
from .models import Notifications
from signup.models import Profile
from django.http import JsonResponse
# Create your views here.


def views_notif(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            print("User views notification")
            user_prfile = Profile.objects.get(user=request.user)
            my_notif = Notifications.objects.filter(receiver=user_prfile, view=False).update(view=True)
            print("Updated Notifications are", my_notif)
            if my_notif:
                data = {"true": True}
            return JsonResponse(data)
