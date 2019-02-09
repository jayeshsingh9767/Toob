from .models import Notifications


def notify(sender, receiver, msg, type):
    if Notifications.objects.filter(
            sender=sender,
            receiver=receiver,
            message=msg,
            type=type).exists() != True:
        notify = Notifications.objects.create(
            sender=sender,
            receiver=receiver,
            message=msg,
            type=type
        )
        notify.save()


def remove_notify(sender, receiver, msg, type):
    if Notifications.objects.filter(
            sender=sender,
            receiver=receiver,
            message=msg,
            type=type).exists():
            Notifications.objects.filter(
                sender=sender,
                receiver=receiver,
                message=msg,
                type=type
            ).delete()
