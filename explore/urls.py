from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.explore, name='explore'),
    path('followers/', views.followers, name='followers'),
    path('followings/', views.followings, name='followings')
]
