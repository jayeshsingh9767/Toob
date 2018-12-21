from django.db import models
from django.contrib.auth.models import User


class Posts(models.Model):
    title = models.CharField(max_length=250, blank=False)
    content = models.CharField(max_length=15000,
                               help_text="Write Your thought here...")
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField(blank=True,
                              help_text="Use Image for Impowring your Thought")
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trending_ratio = models.IntegerField(default=1)
    # down_vote = models.ForeignKey()

    def __str__(self):
        return self.title


class Upvote(models.Model):
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, unique=False)

    def __str__(self):
        user = str(self.user)
        post = str(self.post)
        return user + " upvoted " + post


class Down_vote(models.Model):
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, unique=False)

    def __str__(self):
        user = str(self.user)
        post = str(self.post)

        return user + " Down Voted " + post
