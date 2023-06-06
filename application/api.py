from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializer import *


@api_view(['GET'])
def Dlist(request):
    all_data = Data.objects.all()
    data = ser(all_data, many=True).data
    return Response({'data': data})


class Dataviews(generics.CreateAPIView):

    queryset = Data.objects.all()
    serializer_class = ser

class ETviews(generics.CreateAPIView):

    queryset = ET0o.objects.all()
    serializer_class = serET

class FWIviews(generics.CreateAPIView):

    queryset = ET0o.objects.all()
    serializer_class = serFWI
