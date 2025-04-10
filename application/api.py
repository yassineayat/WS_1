from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializer import *


@api_view(['GET'])
def Dlist(request):
    all_data = ET0o.objects.all().order_by('-id')[:10]
    data = serET(all_data, many=True).data
    return Response({'data': data})


class Dataviews(generics.CreateAPIView):

    queryset = Data.objects.all()
    serializer_class = ser


class Dataviews2(generics.CreateAPIView):

    queryset = Data2.objects.all()
    serializer_class = ser2

class ETviews(generics.CreateAPIView):

    queryset = ET0o.objects.all()
    serializer_class = serET

class FWIviews(generics.CreateAPIView):

    queryset = ET0o.objects.all()
    serializer_class = serFWI



class Rayviews(generics.CreateAPIView):

    queryset = Ray2.objects.all()
    serializer_class = serRay


class Envdataviews(generics.CreateAPIView):

    queryset = Envdata.objects.all()
    serializer_class = serEnv

class Cwsiviews(generics.CreateAPIView):

    queryset = cwsi.objects.all()
    serializer_class = serCwsi

