from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
routers=DefaultRouter()
routers.register("",views.UdnViewsSet)
urlpatterns = [
    path('',views.index),
    path('new/<int:id>/',views.article,name="article"),
    path("Udn_Ajax/",include(routers.urls))
]