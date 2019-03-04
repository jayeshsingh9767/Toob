from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<post_id>[0-9]+)/$', views.details_post, name='details_post'),
    url(r'^comment/(?P<post_id>[0-9]+)/$',
        views.comment_submit, name='comment_submit')
]
