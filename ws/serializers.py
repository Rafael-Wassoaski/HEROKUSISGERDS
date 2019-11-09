from rest_framework import serializers
from relatorios.models import Vistoria
from django.contrib.auth.models import User



class VistoriaSerializer(serializers.Serializer):
    class Meta:
        model = Vistoria
        fields = '__all__'