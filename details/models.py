from django.db import models
from home.models import Posts
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        ans = str(self.user) + ' commentd on ' + str(self.post)
        return ans

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.time_stamp = timezone.now()
        return super(Comment, self).save(*args, **kwargs)
