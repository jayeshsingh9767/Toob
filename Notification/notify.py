from .models import Notifications


def notify(sender, receiver, msg, type, url):
    if sender != receiver:
        if Notifications.objects.filter(
                sender=sender,
                receiver=receiver,
                message=msg,
                type=type,
                redirect_url=url).exists() != True:
            notify = Notifications.objects.create(
                sender=sender,
                receiver=receiver,
                message=msg,
                type=type,
                redirect_url=url
            )
            notify.save()


def remove_notify(sender, receiver, msg, type, url):
    if sender != receiver:
        if Notifications.objects.filter(
                sender=sender,
                receiver=receiver,
                message=msg,
                type=type,
                redirect_url=url).exists():
                Notifications.objects.filter(
                    sender=sender,
                    receiver=receiver,
                    message=msg,
                    type=type,
                    redirect_url=url
                ).delete()
