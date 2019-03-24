from django.urls import path
from django.conf.urls import url
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    path('follow/', views.follow, name='follow'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('edit/submit', views.edit_submit, name='edit_submit')


]
