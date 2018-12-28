from django.db import models
from django.contrib.auth.models import User
from signup.models import Profile


class Posts(models.Model):
    title = models.CharField(max_length=250, blank=False)
    content = models.TextField(max_length=15000,
                               help_text="Write Your thought here...")
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dis_likes = models.ManyToManyField(User, blank=True,
                                       related_name='dis_likes')
    image = models.ImageField(blank=True,
                              help_text="Use Image for Impowring your Thought")
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    trending_ratio = models.IntegerField(default=1)

    def __str__(self):
        return self.title
