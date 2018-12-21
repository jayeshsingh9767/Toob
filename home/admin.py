from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Posts)
admin.site.register(models.Upvote)
admin.site.register(models.Down_vote)
