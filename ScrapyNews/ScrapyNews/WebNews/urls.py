from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
routers=DefaultRouter()
routers.register("",views.UdnViewsSet,basename="article")
urlpatterns = [
    path('',views.index),
    path("<str:id>",views.article),
    path("Udn_Ajax/",include(routers.urls))
]