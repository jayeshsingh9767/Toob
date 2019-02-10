from django.db import models
from signup.models import Profile

# Create your models here.


class Notifications(models.Model):
    choice_type = (
        (50, 'Security'),
        (40, 'Level'),
        (30, 'Info'),
        (20, 'Updates'),
        (10, 'Other')
    )
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
    message = models.CharField(max_length=500, blank=False)
    type = models.CharField(max_length=50, choices=choice_type)
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    redirect_url = models.URLField(max_length=300, blank=True)
    view = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sender) + " " + str(self.message) + " " + str(self.receiver)
