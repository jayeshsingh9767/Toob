from .models import Notifications
from signup.models import Profile


def pass_value(request):
    if request.user.is_authenticated:
        user_prfile = Profile.objects.get(user=request.user)
        my_notif = Notifications.objects.filter(receiver=user_prfile)
        context = {
            "my_notif": my_notif
        }
        return context
    else:
        context = {}
        return context
