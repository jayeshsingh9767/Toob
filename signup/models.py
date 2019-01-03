from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    level = models.IntegerField(default=1, editable=False)
    bio = models.TextField(max_length=410, default='Edit Bio')
    date_of_joining = models.DateTimeField(editable=False,
                                           default=timezone.now)
    follows = models.ManyToManyField('Profile', null=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
