from .models import Notifications
from signup.models import Profile


def pass_value(request):
    if request.user.is_authenticated:
        user_prfile = Profile.objects.get(user=request.user)
        my_notif = Notifications.objects.filter(receiver=user_prfile)
        unseen_notif_count = my_notif.filter(view=False).count()
        count = my_notif.count()
        if count >= 13:
            my_notif = my_notif[count-13:]
        context = {
            "my_notif": my_notif,
            "unseen_notif_count": unseen_notif_count
        }
        return context
    else:
        context = {}
        return context
