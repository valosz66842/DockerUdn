from rest_framework import serializers
from .models import Udn

class UdnSerializers(serializers.ModelSerializer):
    class Meta:
        model=Udn
        fields='__all__'
