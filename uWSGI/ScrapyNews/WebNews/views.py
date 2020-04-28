from django.shortcuts import render
from rest_framework import viewsets
from .models import Udn
from .serializers import UdnSerializers
import os
import sys
pwd=os.path.dirname(__file__)
sys.path.append(pwd+"../kafka_producer.py")
import kafka_producer
import socket
from django.forms.models import model_to_dict
from django.http import JsonResponse
class UdnViewsSet(viewsets.ModelViewSet):
    queryset =Udn.objects.all().order_by('-time')#modles所有資料 並照時間排序
    serializer_class = UdnSerializers #序列化
def index(request):
    os_name=os.name
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()
    return render(request,"index.html", locals())
def record(request):
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.META['REMOTE_ADDR']
    title=request.GET.get("datatitle",None)#透過ajax獲得使用者操作紀錄
    titledict={"title":title}
    kafka_producer.producer(kafka_producer.Els(ip,title))#透過kafka_producer傳送至elk跟mysql做紀錄
    return JsonResponse(titledict)

