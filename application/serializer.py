from rest_framework import serializers
from .models import *

# Serializers define the API representation.
class ser(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'

class serET(serializers.ModelSerializer):
    class Meta:
        model = ET0o
        fields = '__all__'

class serFWI(serializers.ModelSerializer):
    class Meta:
        model = DataFwiO
        fields = '__all__'