from rest_framework import serializers
from .models import *

# Serializers define the API representation.
class ser(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'

class ser2(serializers.ModelSerializer):
    class Meta:
        model = Data2
        fields = '__all__'

class serET(serializers.ModelSerializer):
    class Meta:
        model = ET0o
        fields = '__all__'

class serFWI(serializers.ModelSerializer):
    class Meta:
        model = DataFwiO
        fields = '__all__'

class serRay(serializers.ModelSerializer):
    class Meta:
        model = Ray2
        fields = '__all__'

class serEnv(serializers.ModelSerializer):
    class Meta:
        model = Envdata
        exclude = ['last_calculation_S1','last_calculation_S2','last_calculation_S3']

class serCwsi(serializers.ModelSerializer):
    class Meta:
        model = cwsi
        fields = '__all__'


# class Rayviews(generics.CreateAPIView):

#     queryset = ET0o.objects.all()
#     serializer_class = serRay


# class Envdataviews(generics.CreateAPIView):

#     queryset = Envdata.objects.all()
#     serializer_class = serEnv
