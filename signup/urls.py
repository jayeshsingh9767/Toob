from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    path('follow/', views.follow, name='follow')
]
