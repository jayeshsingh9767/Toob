from django.db import models
from home.models import Posts
from signup.models import Profile

# Create your models here.


class Report(models.Model):
    reasons = (
        ('1', "Adult Content"),
        ('2', 'Misleading Advetisement'),
        ('3', 'Abusives Content'),
        ('4', 'Duplicate Thought'),
        ('5', 'Other')
    )
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reporting_reason = models.CharField(max_length=100, choices=reasons)
    other_reason = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.user) + " reported Thought " + str(self.post)
