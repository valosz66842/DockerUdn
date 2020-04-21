from django.shortcuts import render
from rest_framework import viewsets
from .models import Udn
from .serializers import UdnSerializers
import os
import sys
pwd=os.path.dirname(__file__)
sys.path.append(pwd+"../kafka_producer.py")
import kafka_producer
from django.forms.models import model_to_dict
class UdnViewsSet(viewsets.ModelViewSet):
    queryset =Udn.objects.all().order_by('-time')
    serializer_class = UdnSerializers
def index(request):
    return render(request,"index.html", locals())
def article(request,id):
    Article=Udn.objects.get(id=id)
    b=[]
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.META['REMOTE_ADDR']
    kafka_producer.producer(kafka_producer.Els(ip,(model_to_dict(Article)["title"])))
    return render(request,"article.html", locals())

