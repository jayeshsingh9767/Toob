from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<post_id>[0-9]+)/$', views.report_post, name='report_post')
]
