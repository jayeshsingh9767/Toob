"""toob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from toob import settings
from home import views as views
from signup.views import signup
from logout.views import logout
from django.conf.urls.static import static
from Notification.views import views_notif


urlpatterns = [
    path('admin/', admin.site.urls, name='home'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('signup/', signup, name='signup'),
    path('', views.home, name='home'),
    path('logout/', logout, name='logout'),
    path('like/', views.like_post, name="like_post"),
    path('dislike/', views.dis_like_post, name="dis_like_post"),
    path('details/', include('details.urls')),
    path('profile/', include('signup.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
    path('write_thought', views.write_thought, name="write_thought"),
    path('post_thought', views.post_thought, name="post_thought"),
    path('explore/', include('explore.urls')),
    path('views_notify/', views_notif, name="views_notif"),
    path('temp', views.temp, name="temp"),
    path('admin/analyse/', include('analyse.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
