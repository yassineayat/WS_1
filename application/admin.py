from django.contrib import admin
from django.conf.locale.es import formats as es_formats
from .models import *

admin.site.register(vanne)
admin.site.register(CapSol)
admin.site.register(CapSol2)
admin.site.register(Ws)
admin.site.register(Data)
admin.site.register(ET0)
admin.site.register(DataFwi)
admin.site.register(Ray)

