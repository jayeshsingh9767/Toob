from django.urls import path
from django.conf.urls import url
from .views import (
        analyse,
        user_level,
        toob_growth,
        analyse_post,
        tags,
        select_user,
        analyse_user,
        compare_user
    )
from .apis import get_trend_user_api, get_popular_user, get_user_api

urlpatterns = [
    path('', analyse, name='analyse'),
    path('user', user_level, name='analyse_user_level'),
    path('toob', toob_growth, name='analyse_toob_growth'),
    path('select_user', select_user, name='select_user'),
    url(r'^select_user/(?P<user_id>[0-9]+)/$', analyse_user, name='analyse_user'),
    path('analyse_post', analyse_post, name='analyse_post'),
    url(r'get_user_api/(?P<user_id>[0-9]+)/$', get_user_api, name='get_user'),
    path('select_user/compare', compare_user, name="compare_user"),
    path('tags', tags, name='analyse_tags'),
    path('get_trend_user_api', get_trend_user_api, name="get_user_api"),
    path('get_popular_user', get_popular_user, name="get_popular_user")
]
