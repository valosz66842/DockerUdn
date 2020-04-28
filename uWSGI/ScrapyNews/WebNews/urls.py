from django.urls import path, include,re_path
from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
routers=DefaultRouter()
routers.register("",views.UdnViewsSet)
urlpatterns = [
    path('',views.index),
    path("Udn_Ajax/",include(routers.urls)),
    path("record/",views.record)
]