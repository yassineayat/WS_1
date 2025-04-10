# Create your views here.
import datetime
import math
from django.utils.timezone import localtime
import numpy as np
import pandas as pd
from django.utils import timezone
from django.db.models import Max, Min, Sum, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView
# import paho.mqtt.client as mqtt

from .models import *
import requests
import json

from collections import Counter
from django.http import JsonResponse
# import penmon as pm
#programmation chirpstack
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

WS_DEVEUI_OPENSNZ = '57c32e0eb4160806'
valve_eui= '2ee5270e481778ff'
black_device_eui= '13e08e2951742243'
red_device_eui= '6f8e5550f7ec89e9'
npk_device_eui= 'fe86cac7b467a956'
pyranometre = '71ca6b16b8e4ac42'
pyranometre_jaune = '18362e0eb4160834'
WsSENSECAP_WeatherStation = '2cf7f1c04430038d'
module_drajino = 'a84041834189a939'
pyraGV = 'a84041fc4188657b'

Capteurdesol ='a84041d10858e027'
#fin progra

def aqi(request):
    context={}
    return render(request,"tab.html",context)

def chart(request):
    tab=CapSol.objects.all()
    labels = []
    dataa = []
    dataa2 = []
    for data in tab:
        labels.append((data.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(data.Temp)
        dataa2.append(data.Hum)
        print("labels0", type(labels))
    if (request.method == "POST"):
        labels.clear()
        dataa.clear()
        dataa2.clear()

        fromdate = request.POST.get('startdate')
        # print(type(datetime.datetime.now()))
        print("fromdate")
        print(fromdate)
        todate = request.POST.get('enddate')
        print("todate")
        print(todate)
        first = CapSol.objects.first()
        print("first date", str(first.dt))
        lastdate = CapSol.objects.last()
        print("last date", str(lastdate.dt))
        if fromdate != "" and todate != "":
            # to = datetime.datetime.strptime(todate, '%Y-%m-%d')+datetime.timedelta(days=1)
            to = datetime.datetime.strptime(todate, '%Y-%m-%d') + datetime.timedelta(days=1)
            print("to", to)
            # fromdate = datetime.datetime("07-07")
            created_documents5 = CapSol.objects.filter(dt__range=[fromdate, to]).order_by('dt')
            print("created_documents5", created_documents5)
            for data in created_documents5:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Temp)
                dataa2.append(data.Hum)
                print("labelfiltter", labels)
                # return HttpResponseRedirect('/')
            # print("labelfiltter",labels)
        if fromdate == "":
            fromdate = first.dt

        if todate == "":
            to = (lastdate.dt) + datetime.timedelta(days=1)
            todate = to + datetime.timedelta(days=1)
            labels.clear()
            dataa.clear()
            dataa2.clear()
            created_documents6 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('id')
            # print("created_documents6", created_documents6)

            for data in created_documents6:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Temp)
                dataa2.append(data.Hum)
                # print("lab", labels)
                return HttpResponseRedirect('/Chart')

            print("todate", type(todate))

    context={'tab':tab,'labels':labels,'dataa':dataa}
    return render(request,"charts.html",context)


""" temperature capteur de sol"""
def tsol1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print((datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0))
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Tsol1.html", context)

def tsol3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Tsol3.html", context)

def tsol7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Tsol7.html", context)

def tsol15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Tsol15.html", context)

def tsol21(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Tsol1.html", context)

def tsol23(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Tsol3.html", context)

def tsol27(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Tsol7.html", context)

def tsol215(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Tsol15.html", context)

""" humidité sol """
def hsol1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Hsol1.html", context)

def hsol3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Hsol3.html", context)

def hsol7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Hsol7.html", context)

def hsol15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Hsol15.html", context)

def hsol21(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Hsol1.html", context)

def hsol23(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Hsol3.html", context)

def hsol27(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Hsol7.html", context)

def hsol215(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Hsol15.html", context)


def ssol1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Sal)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Ssol1.html", context)

def ssol3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Sal)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Ssol3.html", context)

def ssol7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Sal)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Ssol7.html", context)

def ssol15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Sal)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Ssol15.html", context)

def ssol21(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Sal)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Ssol1.html", context)

def ssol23(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Sal)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Ssol3.html", context)

def ssol27(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Sal)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Ssol7.html", context)

def ssol215(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Sal)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Ssol15.html", context)

# EC
def esol1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ec)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Esol1.html", context)

def esol3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        #print("labels", labels)
        dataa.append(i.Ec)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Esol3.html", context)

def esol7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ec)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Esol7.html", context)

def esol15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ec)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Esol15.html", context)

""" e2"""

def esol21(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ec)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Esol1.html", context)

def esol23(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ec)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Esol3.html", context)

def esol27(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ec)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Esol7.html", context)

def esol215(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ec)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Esol15.html", context)

#N
def nsol1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs de l'azote (N)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.N)  # Utilisation de N pour l'azote

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Nsol1.html", context)

def nsol3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs de l'azote (N)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.N)  # Utilisation de N pour l'azote
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Nsol3.html", context)

def nsol7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs de l'azote (N)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.N)  # Utilisation de N pour l'azote
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Nsol7.html", context)

def nsol15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs de l'azote (N)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.N)  # Utilisation de N pour l'azote
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Nsol15.html", context)

def nsol21(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs de l'azote (N)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.N)  # Utilisation de N pour l'azote
    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Nsol1.html", context)

def nsol23(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs de l'azote (N)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.N)  # Utilisation de N pour l'azote
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Nsol3.html", context)

def nsol27(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs de l'azote (N)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.N)  # Utilisation de N pour l'azote
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Nsol7.html", context)

def nsol215(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs de l'azote (N)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.N)  # Utilisation de N pour l'azote
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Nsol15.html", context)

#P
def psol1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du phosphore (P)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.P)  # Utilisation de P pour le phosphore

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Psol1.html", context)

def psol3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du phosphore (P)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.P)  # Utilisation de P pour le phosphore
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Psol3.html", context)

def psol7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du phosphore (P)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.P)  # Utilisation de P pour le phosphore
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Psol7.html", context)

def psol15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du phosphore (P)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.P)  # Utilisation de P pour le phosphore
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Psol15.html", context)

def psol21(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du phosphore (P)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.P)  # Utilisation de P pour le phosphore
    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Psol1.html", context)

def psol23(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du phosphore (P)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.P)  # Utilisation de P pour le phosphore
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Psol3.html", context)

def psol27(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du phosphore (P)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.P)  # Utilisation de P pour le phosphore
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Psol7.html", context)

def psol215(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du phosphore (P)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.P)  # Utilisation de P pour le phosphore
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Psol15.html", context)

#K
def ksol1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du potassium (K)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.K)  # Utilisation de K pour le potassium

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Ksol1.html", context)

def ksol3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du potassium (K)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.K)  # Utilisation de K pour le potassium
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Ksol3.html", context)

def ksol7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du potassium (K)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.K)  # Utilisation de K pour le potassium
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Ksol7.html", context)

def ksol15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du potassium (K)
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.K)  # Utilisation de K pour le potassium
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Ksol15.html", context)

def ksol21(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du potassium (K)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.K)  # Utilisation de K pour le potassium
    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Ksol1.html", context)

def ksol23(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du potassium (K)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.K)  # Utilisation de K pour le potassium
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Ksol3.html", context)

def ksol27(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du potassium (K)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.K)  # Utilisation de K pour le potassium
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Ksol7.html", context)

def ksol215(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []  # Contiendra les valeurs du potassium (K)
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(i.K)  # Utilisation de K pour le potassium
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Ksol15.html", context)

#Batterie
def bsol1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Bsol1.html", context)

def bsol3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Bsol3.html", context)

def bsol7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Bsol7.html", context)

def bsol15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol2.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol/Bsol15.html", context)

def bsol21(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Bsol1.html", context)

def bsol23(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Bsol3.html", context)

def bsol27(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Bsol7.html", context)

def bsol215(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = CapSol.objects.filter(dt__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.dt).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "sol2/Bsol15.html", context)
""" fin sol """

#temperature

def dash(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "temp/Tempjrs.html", context)

def data3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "temp/Temp3jrs.html", context)

def data7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "temp/Temp7jrs.html", context)

def data15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Temp)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "temp/Temp15jrs.html", context)


#humidité
def hum1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "hum/hum1.html", context)

def hum3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "hum/hum3.html", context)

def hum7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "hum/hum7.html", context)

def hum15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Hum)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "hum/hum15.html", context)
""" fin hum"""

#vitesse
def vit1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    # print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Wind_Speed)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "vite/vit1.html", context)

def vit3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Wind_Speed)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "vite/vit3.html", context)

def vit7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Wind_Speed)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "vite/vit7.html", context)

def vit15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Wind_Speed)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "vite/vit15.html", context)
""" fin vit"""

#rayonnement
def ray1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    # print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = Ray2.objects.filter(DateRay__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.DateRay).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ray)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "ray/ray1.html", context)

def ray3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Ray2.objects.filter(DateRay__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.DateRay).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ray)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "ray/ray3.html", context)

def ray7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Ray2.objects.filter(DateRay__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.DateRay).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ray)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "ray/ray7.html", context)

def ray15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Ray2.objects.filter(DateRay__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.DateRay).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ray)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "ray/ray15.html", context)
""" fin ray"""

#pluviemetre
def plu1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Rain)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "plu/plu1.html", context)

def plu3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Rain)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "plu/plu3.html", context)

def plu7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Rain)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "plu/plu7.html", context)

def plu15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Rain)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "plu/plu15.html", context)
""" fin plu"""

#batterie
def bat1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "bat/bat1.html", context)

def bat3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "bat/bat3.html", context)

def bat7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "bat/bat7.html", context)

def bat15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data2.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "bat/bat15.html", context)
""" fin bat"""
#batterie
def bat11(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0,minute=0,second=0,microsecond=0)
    print("oui ......",one_day_ago)
    labels = []
    dataa = []
    all = Ray2.objects.filter(DateRay__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.DateRay).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "batt/bat1.html", context)

def bat31(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Ray2.objects.filter(DateRay__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.DateRay).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "batt/bat3.html", context)

def bat71(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Ray2.objects.filter(DateRay__gte=one_day_ago)
    print("all", all)
    for i in all:
        labels.append((i.DateRay).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "batt/bat7.html", context)

def bat151(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Ray2.objects.filter(DateRay__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.DateRay).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "batt/bat15.html", context)
""" fin bat"""

def et(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = ET0o.objects.filter(Time_Stamp__gte=one_day_ago)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d "))
        dataa.append(i.value)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "ET0/et.html", context)


def et0(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = ET0.objects.filter(Time_Stamp__gte=one_day_ago)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d "))
        dataa.append(i.value)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "ET0/et0.html", context)

def fwi0(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = DataFwiO.objects.filter(Time_Stamp__gte=one_day_ago)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d "))
        dataa.append(i.fwi)

    context = {'all': all, 'labels': labels, 'dataa': dataa}
    return render(request, "fwi/fwi.html", context)


def charthum(request):
    tab=CapSol.objects.all()
    labels = []
    dataa = []
    dataa2 = []
    for data in tab:
        labels.append((data.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(data.Temp)
        dataa2.append(data.Hum)
        print("labels0", type(labels))
    if (request.method == "POST"):
        labels.clear()
        dataa.clear()
        dataa2.clear()

        fromdate = request.POST.get('startdate')
        # print(type(datetime.datetime.now()))
        print("fromdate")
        print(fromdate)
        todate = request.POST.get('enddate')
        print("todate")
        print(todate)
        first = CapSol.objects.first()
        print("first date", str(first.dt))
        lastdate = CapSol.objects.last()
        print("last date", str(lastdate.dt))
        if fromdate != "" and todate != "":
            # to = datetime.datetime.strptime(todate, '%Y-%m-%d')+datetime.timedelta(days=1)
            to = datetime.datetime.strptime(todate, '%Y-%m-%d') + datetime.timedelta(days=1)
            print("to", to)
            # fromdate = datetime.datetime("07-07")
            created_documents5 = CapSol.objects.filter(dt__range=[fromdate, to]).order_by('dt')
            print("created_documents5", created_documents5)
            for data in created_documents5:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Temp)
                dataa2.append(data.Hum)
                print("labelfiltter", labels)
                # return HttpResponseRedirect('/')
            # print("labelfiltter",labels)
        if fromdate == "":
            fromdate = first.dt

        if todate == "":
            to = (lastdate.dt) + datetime.timedelta(days=1)
            todate = to + datetime.timedelta(days=1)
            labels.clear()
            dataa.clear()
            dataa2.clear()
            created_documents6 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('id')
            print("created_documents6", created_documents6)

            for data in created_documents6:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Temp)
                dataa2.append(data.Hum)
                print("lab", labels)
                return HttpResponseRedirect('/Charthum')

            print("todate", type(todate))

    context={'tab':tab,'labels':labels,'dataa':dataa,'dataa2':dataa2}
    return render(request,"chartshum.html",context)
"""
def chartsal(request):
    tab=CapSol.objects.all()
    labels = []
    dataa = []
    for data in tab:
        labels.append((data.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(data.Sal)
        print("labels0", type(labels))
    if (request.method == "POST"):
        labels.clear()
        dataa.clear()

        fromdate = request.POST.get('startdate')
        # print(type(datetime.datetime.now()))
        print("fromdate")
        print(fromdate)
        todate = request.POST.get('enddate')
        print("todate")
        print(todate)
        first = CapSol.objects.first()
        print("first date", str(first.dt))
        lastdate = CapSol.objects.last()
        print("last date", str(lastdate.dt))
        if fromdate != "" and todate != "":
            # to = datetime.datetime.strptime(todate, '%Y-%m-%d')+datetime.timedelta(days=1)
            to = datetime.datetime.strptime(todate, '%Y-%m-%d') + datetime.timedelta(days=1)
            print("to", to)
            # fromdate = datetime.datetime("07-07")
            created_documents5 = CapSol.objects.filter(dt__range=[fromdate, to]).order_by('dt')
            print("created_documents5", created_documents5)
            for data in created_documents5:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Sal)

                print("labelfiltter", labels)
                # return HttpResponseRedirect('/')
            # print("labelfiltter",labels)
        if fromdate == "":
            fromdate = first.dt

        if todate == "":
            to = (lastdate.dt) + datetime.timedelta(days=1)
            todate = to + datetime.timedelta(days=1)
            labels.clear()
            dataa.clear()

            created_documents6 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('id')
            print("created_documents6", created_documents6)

            for data in created_documents6:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Sal)

                print("lab", labels)
                return HttpResponseRedirect('/Chartsal')

            print("todate", type(todate))

    context={'tab':tab,'labels':labels,'dataa':dataa}
    return render(request,"chartssal.html",context)
"""
def chartN(request):
    tab=CapSol.objects.all()
    labels = []
    dataa = []
    for data in tab:
        labels.append((data.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(data.N)
        print("labels0", type(labels))
    if (request.method == "POST"):
        labels.clear()
        dataa.clear()

        fromdate = request.POST.get('startdate')
        # print(type(datetime.datetime.now()))
        print("fromdate")
        print(fromdate)
        todate = request.POST.get('enddate')
        print("todate")
        print(todate)
        first = CapSol.objects.first()
        print("first date", str(first.dt))
        lastdate = CapSol.objects.last()
        print("last date", str(lastdate.dt))
        if fromdate != "" and todate != "":
            # to = datetime.datetime.strptime(todate, '%Y-%m-%d')+datetime.timedelta(days=1)
            to = datetime.datetime.strptime(todate, '%Y-%m-%d') + datetime.timedelta(days=1)
            print("to", to)
            # fromdate = datetime.datetime("07-07")
            created_documents5 = CapSol.objects.filter(dt__range=[fromdate, to]).order_by('dt')
            print("created_documents5", created_documents5)
            for data in created_documents5:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.N)

                print("labelfiltter", labels)
                # return HttpResponseRedirect('/')
            # print("labelfiltter",labels)
        if fromdate == "":
            fromdate = first.dt

        if todate == "":
            to = (lastdate.dt) + datetime.timedelta(days=1)
            todate = to + datetime.timedelta(days=1)
            labels.clear()
            dataa.clear()

            created_documents6 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('id')
            print("created_documents6", created_documents6)

            for data in created_documents6:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.N)

                print("lab", labels)
                return HttpResponseRedirect('/ChartN')

            print("todate", type(todate))

    context={'tab':tab,'labels':labels,'dataa':dataa}
    return render(request,"chartsN.html",context)

def chartP(request):
    tab=CapSol.objects.all()
    labels = []
    dataa = []
    for data in tab:
        labels.append((data.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(data.P)
        print("labels0", type(labels))
    if (request.method == "POST"):
        labels.clear()
        dataa.clear()

        fromdate = request.POST.get('startdate')
        # print(type(datetime.datetime.now()))
        print("fromdate")
        print(fromdate)
        todate = request.POST.get('enddate')
        print("todate")
        print(todate)
        first = CapSol.objects.first()
        print("first date", str(first.dt))
        lastdate = CapSol.objects.last()
        print("last date", str(lastdate.dt))
        if fromdate != "" and todate != "":
            # to = datetime.datetime.strptime(todate, '%Y-%m-%d')+datetime.timedelta(days=1)
            to = datetime.datetime.strptime(todate, '%Y-%m-%d') + datetime.timedelta(days=1)
            print("to", to)
            # fromdate = datetime.datetime("07-07")
            created_documents5 = CapSol.objects.filter(dt__range=[fromdate, to]).order_by('dt')
            print("created_documents5", created_documents5)
            for data in created_documents5:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.P)

                print("labelfiltter", labels)
                # return HttpResponseRedirect('/')
            # print("labelfiltter",labels)
        if fromdate == "":
            fromdate = first.dt

        if todate == "":
            to = (lastdate.dt) + datetime.timedelta(days=1)
            todate = to + datetime.timedelta(days=1)
            labels.clear()
            dataa.clear()

            created_documents6 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('id')
            print("created_documents6", created_documents6)

            for data in created_documents6:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.P)

                print("lab", labels)
                return HttpResponseRedirect('/ChartP')

            print("todate", type(todate))

    context={'tab':tab,'labels':labels,'dataa':dataa}
    return render(request,"chartsP.html",context)

def chartK(request):
    tab=CapSol.objects.all()
    labels = []
    dataa = []
    for data in tab:
        labels.append((data.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(data.K)
        print("labels0", type(labels))
    if (request.method == "POST"):
        labels.clear()
        dataa.clear()

        fromdate = request.POST.get('startdate')
        # print(type(datetime.datetime.now()))
        print("fromdate")
        print(fromdate)
        todate = request.POST.get('enddate')
        print("todate")
        print(todate)
        first = CapSol.objects.first()
        print("first date", str(first.dt))
        lastdate = CapSol.objects.last()
        print("last date", str(lastdate.dt))
        if fromdate != "" and todate != "":
            # to = datetime.datetime.strptime(todate, '%Y-%m-%d')+datetime.timedelta(days=1)
            to = datetime.datetime.strptime(todate, '%Y-%m-%d') + datetime.timedelta(days=1)
            print("to", to)
            # fromdate = datetime.datetime("07-07")
            created_documents5 = CapSol.objects.filter(dt__range=[fromdate, to]).order_by('dt')
            print("created_documents5", created_documents5)
            for data in created_documents5:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.K)

                print("labelfiltter", labels)
                # return HttpResponseRedirect('/')
            # print("labelfiltter",labels)
        if fromdate == "":
            fromdate = first.dt

        if todate == "":
            to = (lastdate.dt) + datetime.timedelta(days=1)
            todate = to + datetime.timedelta(days=1)
            labels.clear()
            dataa.clear()

            created_documents6 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('id')
            print("created_documents6", created_documents6)

            for data in created_documents6:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.K)

                print("lab", labels)
                return HttpResponseRedirect('/ChartK')

            print("todate", type(todate))

    context={'tab':tab,'labels':labels,'dataa':dataa}
    return render(request,"chartsK.html",context)

def chartbat(request):
    tab=CapSol.objects.all()
    labels = []
    dataa = []
    for data in tab:
        labels.append((data.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(data.Bat)
        print("labels0", type(labels))
    if (request.method == "POST"):
        labels.clear()
        dataa.clear()

        fromdate = request.POST.get('startdate')
        # print(type(datetime.datetime.now()))
        print("fromdate")
        print(fromdate)
        todate = request.POST.get('enddate')
        print("todate")
        print(todate)
        first = CapSol.objects.first()
        print("first date", str(first.dt))
        lastdate = CapSol.objects.last()
        print("last date", str(lastdate.dt))
        if fromdate != "" and todate != "":
            # to = datetime.datetime.strptime(todate, '%Y-%m-%d')+datetime.timedelta(days=1)
            to = datetime.datetime.strptime(todate, '%Y-%m-%d') + datetime.timedelta(days=1)
            print("to", to)
            # fromdate = datetime.datetime("07-07")
            created_documents5 = CapSol.objects.filter(dt__range=[fromdate, to]).order_by('dt')
            print("created_documents5", created_documents5)
            for data in created_documents5:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Bat)

                print("labelfiltter", labels)
                # return HttpResponseRedirect('/')
            # print("labelfiltter",labels)
        if fromdate == "":
            fromdate = first.dt

        if todate == "":
            to = (lastdate.dt) + datetime.timedelta(days=1)
            todate = to + datetime.timedelta(days=1)
            labels.clear()
            dataa.clear()

            created_documents6 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('id')
            print("created_documents6", created_documents6)

            for data in created_documents6:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Bat)

                print("lab", labels)
                return HttpResponseRedirect('/Chartec')

            print("todate", type(todate))

    context={'tab':tab,'labels':labels,'dataa':dataa}
    return render(request,"chartsbat.html",context)


def exemple():
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).replace(hour=0,minute=0,second=0,microsecond=0)
    now=(datetime.datetime.now()).replace(hour=0,minute=0,second=0,microsecond=0)
    onedayRay = one_day_ago.replace(hour=7)
    todayRay = one_day_ago.replace(hour=20)
    posts = Ws.objects.filter(date__gte=one_day_ago,date__lte=now)
    hm = Ws.objects.filter(date__gte=one_day_ago, date__lte=now,Humidity__gte=50)
    print("hm :",hm)
    # print("posts ws", posts.count())
    print("heure", one_day_ago)
    print("to heure", todayRay)

    post = Ray.objects.filter(DateRay__gte=one_day_ago, DateRay__lte=now)
    rav = post.count()
    print("nbrs ray1", rav)
    print("____________________________________filtre par heure _______________________________________")

    filtresup=Ray.objects.filter(DateRay__gte=onedayRay,DateRay__lte=todayRay)
    print("filtre nbr:",filtresup.count())
    w=filtresup.aggregate(Sum('Ray'))
    print("filtreRay :", w)
    rayonnement = w['Ray__sum']/rav
    print("avreage ray :", rayonnement)
    print("_____________________________________fin filtre par heure __________________________________")

    totalRay = post.values('Ray').aggregate(Sum('Ray'))
    Maxtemp = posts.values('Temperature').aggregate(Max('Temperature'))
    Mintemp = posts.values('Temperature').aggregate(Min('Temperature'))
    MaxHum = posts.values('Humidity').aggregate(Max('Humidity'))
    MinHum = posts.values('Humidity').aggregate(Min('Humidity'))
    avreage = posts.aggregate(Avg('Vent'))
    dicttolistVent = list(avreage.items())
    avgvent = (round(dicttolistVent[0][1] / 3.6, 4))
    vitvent = round(dicttolistVent[0][1],4)
    print("vitvent :",vitvent)
    dicttolisTmax = list(Maxtemp.items())
    Tmmax = dicttolisTmax[0][1]
    dicttolisTmin = list(Mintemp.items())
    Tmmin = dicttolisTmin[0][1]
    dicttolisHmax = list(MaxHum.items())
    Hmax = dicttolisHmax[0][1]
    dicttolisHmin = list(MinHum.items())
    Hmin = dicttolisHmin[0][1]
    # print("posts", posts)
    print("tv", avgvent)
    print("tr", totalRay)
    print("tmin", Tmmin)
    print("tmax", Tmmax)
    print("hmin", Hmin)
    print("hmax", Hmax)
    print("avg :", avgvent)
    B2 = one_day_ago.timetuple().tm_yday # 57#
    print("b2", B2)
    RS = 6017.33  # totl radiation
    Tmin = Tmmin#6.62#
    Tmax = Tmmax#29.19#
    HRmin = Hmin #16.46#
    HRmax = Hmax #74.86#
    u = avgvent  # m/s moyen 0.1652#

    print("--------------------------------------------------------------")
    station = pm.Station(latitude=33.9, altitude=1690)
    station.anemometer_height = 2
    r = round(180.2 * 0.0864, 2)
    print(r)
    day = station.day_entry(B2,
                            temp_min=11.76,
                            temp_max=24.66,
                            wind_speed=u,
                            humidity_min=43.77,
                            humidity_max= 92.33,
                            # humidity_mean=(HRmin+HRmax)*0.5,
                            radiation_s=r,
                            )
    print("ETo for this day is", day.eto())
    print("--------------------------------------------------------------")

    M = round(rayonnement,2)  # radiation/h RS/24#
    print("ray ", M)
    N = round(M * 3600 * 0.000001 * 24,2)  # Rs [MJm-2d-1]
    print("N :",N)
    u2 = round(u * 4.87 / math.log(67.8 * 2 - 5.42),3)
    print("u2 ;",u2)
    latitude = 53.9
    altitude = 580
    ctesolaire = 0.082
    StefanBolt = 0.000000004896
    p = 3.140
    g = 0.000665 * 101.3 * math.pow(((293 - 0.0065 * altitude) / 293), 5.26)
    conversion = latitude * 3.1416 / 180
    Y = 1 + 0.033 * math.cos((2 * p * B2) / 365)
    Z = 0.409 * math.sin((2 * p * B2 / 365) - 1.39)
    AA = math.acos(-math.tan(conversion) * math.tan(Z))
    AB = (24 * 60 / p) * ctesolaire * Y * (
            AA * math.sin(conversion) * math.sin(Z) + math.cos(conversion) * math.cos(Z) * math.sin(AA))
    AC = AB * (0.75 + 0.00002 * altitude)
    AD = 1.35 * (N / AC) - 0.35
    AE = (0.6108 * math.exp(17.27 * Tmin / (Tmin + 237.3)) + 0.6108 * math.exp(17.27 * Tmax / (Tmax + 237.3))) / 2
    AF = (HRmin * 0.6108 * math.exp(17.27 * Tmax / (Tmax + 237.3)) + HRmax * 0.6108 * math.exp(
        17.27 * Tmin / (Tmin + 237.3))) / (2 * 100)
    AG = StefanBolt * 0.5 * ((Tmin + 273) ** 4 + (Tmax + 273) ** 4) * (0.34 - 0.14 * math.sqrt(AF)) * AD
    AH = (1 - 0.23) * N - AG
    AI = 0
    AJ = 4098 * 0.6108 * math.exp(17.27 * 0.5 * (Tmin + Tmax) / (0.5 * (Tmin + Tmax) + 237.3)) / (
            0.5 * (Tmin + Tmax) + 237.3) ** 2
    ET_0 = (0.408 * AJ * (AH - AI) + (1600 * g / ((Tmin + Tmax) * 0.5 + 273)) * u2 * (AE - AF)) / (
            AJ + g * (1 + 0.38 * u2))

    print("ETvisio_0",round(ET_0, 2))

def fwi():
    global temp, rhum, prcp, wind, ffmc0, dc0, dmc0, ffmc, dmc, isi, bui, fwi, i, jprcp
    global DataFWI

    class FWICLASS:
        def __init__(self, temp, rhum, wind, prcp):
            self.h = rhum
            self.t = temp
            self.w = wind
            self.p = prcp

        def FFMCcalc(self, ffmc0):
            mo = (147.2 * (101.0 - ffmc0)) / (59.5 + ffmc0)  # *Eq. 1*#
            if (self.p > 0.5):
                rf = self.p - 0.5  # *Eq. 2*#
                if (mo > 150.0):
                    mo = (mo + 42.5 * rf * math.exp(-100.0 / (251.0 - mo)) * (1.0 - math.exp(-6.93 / rf))) + (
                            .0015 * (mo - 150.0) ** 2) * math.sqrt(rf)  # *Eq. 3b*#
                elif mo <= 150.0:
                    mo = mo + 42.5 * rf * math.exp(-100.0 / (251.0 - mo)) * (1.0 - math.exp(-6.93 / rf))  # *Eq. 3a*#
                if (mo > 250.0):
                    mo = 250.0
            ed = .942 * (self.h ** .679) + (11.0 * math.exp((self.h - 100.0) / 10.0)) + 0.18 * (21.1 - self.t) * (
                    1.0 - 1.0 / math.exp(.1150 * self.h))  # *Eq. 4*#
            if (mo < ed):
                ew = .618 * (self.h ** .753) + (10.0 * math.exp((self.h - 100.0) / 10.0)) + .18 * (21.1 - self.t) * (
                        1.0 - 1.0 / math.exp(.115 * self.h))
                if (mo <= ew):
                    kl = .424 * (1.0 - ((100.0 - self.h) / 100.0) ** 1.7) + (.0694 * math.sqrt(self.w)) * (
                            1.0 - ((100.0 - self.h) / 100.0) ** 8)  # *Eq. 7a*#
                    kw = kl * (.581 * math.exp(.0365 * self.t))  # *Eq. 7b*#
                    m = ew - (ew - mo) / 10.0 ** kw  # *Eq. 9*#
                elif mo > ew:
                    m = mo
            elif (mo == ed):
                m = mo
            elif mo > ed:
                kl = .424 * (1.0 - (self.h / 100.0) ** 1.7) + (.0694 * math.sqrt(self.w)) * (
                        1.0 - (self.h / 100.0) ** 8)  # *Eq. 6a*#
                kw = kl * (.581 * math.exp(.0365 * self.t))  # *Eq. 6b*#
                m = ed + (mo - ed) / 10.0 ** kw  # *Eq. 8*#
            ffmc = (59.5 * (250.0 - m)) / (147.2 + m)
            if (ffmc > 101.0):
                ffmc = 101.0
            if (ffmc <= 0.0):
                ffmc = 0.0
            return ffmc

        def DMCcalc(self, dmc0, mth):
            el = [6.5, 7.5, 9.0, 12.8, 13.9, 13.9, 12.4, 10.9, 9.4, 8.0, 7.0, 6.0]
            t = self.t
            if (t < -1.1):
                t = -1.1
            rk = 1.894 * (t + 1.1) * (100.0 - self.h) * (el[mth - 1] * 0.0001)
            if self.p > 1.5:
                ra = self.p
                rw = 0.92 * ra - 1.27
                wmi = 20.0 + 280.0 / math.exp(0.023 * dmc0)
                if dmc0 <= 33.0:
                    b = 100.0 / (0.5 + 0.3 * dmc0)
                elif dmc0 > 33.0:
                    if dmc0 <= 65.0:
                        b = 14.0 - 1.3 * math.log(dmc0)
                    elif dmc0 > 65.0:
                        b = 6.2 * math.log(dmc0) - 17.2
                wmr = wmi + (1000 * rw) / (48.77 + b * rw)
                pr = 43.43 * (5.6348 - math.log(wmr - 20.0))
            elif self.p <= 1.5:
                pr = dmc0
            if (pr < 0.0):
                pr = 0.0
            dmc = pr + rk
            if (dmc <= 1.0):
                dmc = 1.0
            return dmc

        def DCcalc(self, dc0, mth):
            fl = [-1.6, -1.6, -1.6, 0.9, 3.8, 5.8, 6.4, 5.0, 2.4, 0.4, -1.6, -1.6]
            t = self.t
            if (t < -2.8):
                t = -2.8
            pe = (0.36 * (t + 2.8) + fl[mth - 1]) / 2
            if pe <= 0.0:
                pe = 0.0
            # *Eq. 22*#
            if (self.p > 2.8):
                ra = self.p
                rw = 0.83 * ra - 1.27
                smi = 800.0 * math.exp(-dc0 / 400.0)  # *Eq. 19*#
                dr = dc0 - 400.0 * math.log(1.0 + ((3.937 * rw) / smi))  # *Eqs. 20 and 21*#
                if (dr > 0.0):
                    dc = dr + pe
            elif self.p <= 2.8:
                dc = dc0 + pe
            return dc

        def ISIcalc(self, ffmc):
            mo = 147.2 * (101.0 - ffmc) / (59.5 + ffmc)
            ff = 19.115 * math.exp(mo * -0.1386) * (1.0 + (mo ** 5.31) / 49300000.0)
            isi = ff * math.exp(0.05039 * self.w)
            return isi

        def BUIcalc(self, dmc, dc):
            if dmc <= 0.4 * dc:
                bui = (0.8 * dc * dmc) / (dmc + 0.4 * dc)
            else:
                bui = dmc - (1.0 - 0.8 * dc / (dmc + 0.4 * dc)) * (0.92 + (0.0114 * dmc) ** 1.7)
            if bui < 0.0:
                bui = 0.0
            return bui

        def FWIcalc(self, isi, bui):
            if bui <= 80.0:
                bb = 0.1 * isi * (0.626 * bui ** 0.809 + 2.0)

            else:
                bb = 0.1 * isi * (1000.0 / (25. + 108.64 / math.exp(0.023 * bui)))
            if (bb <= 1.0):
                fwi = bb
            else:
                fwi = math.exp(2.72 * (0.434 * math.log(bb)) ** 0.647)
            return fwi

    def main():
        one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        posts = Ws.objects.filter(date__gte=one_day_ago)
        print("posts :", posts)
        # vent calcul
        totalVent = posts.values('Vent').aggregate(Sum('Vent'))
        nbrVent = posts.values('Vent').count()
        wind = round((totalVent["Vent__sum"] / nbrVent), 2)
        print("totalevent : ", totalVent, nbrVent, wind)
        # temperature calcul
        Maxtemp = posts.values('Temperature').aggregate(Max('Temperature'))
        Mintemp = posts.values('Temperature').aggregate(Min('Temperature'))
        temp = (Maxtemp["Temperature__max"] + Mintemp["Temperature__min"]) / 2
        print("moyTemp :", moyTemp)
        # humiidity calcul
        MaxHum = posts.values('Humidity').aggregate(Max('Humidity'))
        MinHum = posts.values('Humidity').aggregate(Min('Humidity'))
        rhum = (MaxHum["Humidity__max"] + MinHum["Humidity__min"]) / 2
        print("moyHum : ", rhum)
        if rhum > 100.0:
            rhum = 100.0
        # pluie calcul
        totalrain = posts.values('Pluv').aggregate(Sum('Pluv'))
        nmbrRain = posts.values('Pluv').count()
        prcp = totalrain['Pluv__sum'] / nmbrRain
        print("moyRain :", prcp)
        initfw = DataFwi.objects.filter(timestamp__date=one_day_ago)
        ffmc0 = initfw.ffmc
        print("ffmc0 :",ffmc0)
        dmc0 = initfw.dmc
        print("dmc0 :", dmc0)
        dc0 = initfw.dc
        print("dc0 :", dc0)
        mth = datetime.datetime.today().month
        print(mth)#4
        fwisystem = FWICLASS(temp, rhum, wind, prcp)
        ffmc = fwisystem.FFMCcalc(ffmc0)
        dmc = fwisystem.DMCcalc(dmc0, mth)
        dc = fwisystem.DCcalc(dc0, mth)
        isi = fwisystem.ISIcalc(ffmc)
        bui = fwisystem.BUIcalc(dmc, dc)
        fwi = fwisystem.FWIcalc(isi, bui)
        DataFwi.objects.create(ffmc=round(ffmc,1), dmc=round(dmc,1), dc=round(dc,1), isi=round(isi,1), bui=round(bui,1), fwi=round(fwi,2))

def weatherS(request):
    lst=Ws.objects.last()
    t = round(lst.Temperature,1)
    h = round(lst.Humidity)
    v = round(lst.Vent,1)
    r = round(lst.Rafale,1)
    p = round(lst.Pluv,1)

    lstR=Ray.objects.last()
    ray = round(lstR.Ray, 1)
    print(ray)
    lstet = ET0.objects.last()
    lstfwi= DataFwi.objects.last()

    # exemple()
    # FWI
    one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    posts = Ws.objects.filter(date__gte=one_day_ago)
    print("................................. weeather station visio green .................................")
    # #vent calcul
    # totalVent = posts.values('Vent').aggregate(Sum('Vent'))
    # nbrVent = posts.values('Vent').count()
    # moyVent=round((totalVent["Vent__sum"]/nbrVent),2)
    # print("totalevent : ",totalVent , nbrVent, moyVent)
    # #temperature calcul
    # Maxtemp = posts.values('Temperature').aggregate(Max('Temperature'))
    # Mintemp = posts.values('Temperature').aggregate(Min('Temperature'))
    # moyTemp = (Maxtemp["Temperature__max"] + Mintemp["Temperature__min"]) / 2
    # print("moyTemp :", moyTemp)
    # #humiidity calcul
    # MaxHum = posts.values('Humidity').aggregate(Max('Humidity'))
    # MinHum = posts.values('Humidity').aggregate(Min('Humidity'))
    # moyHum = (MaxHum["Humidity__max"] + MinHum["Humidity__min"]) / 2
    # print("moyHum : ", moyHum)
    # #pluie calcul
    # totalrain = posts.values('Pluv').aggregate(Sum('Pluv'))
    # nmbrRain = posts.values('Pluv').count()
    # moyRain = totalrain['Pluv__sum']/nmbrRain
    # print("moyRain :", moyRain)
    # mth = datetime.datetime.today().month
    # print(mth)
    context={'lst':lst,'t':t,'h':h,'v':v,'r':r,'p':p,"lstet":lstet,'lstfwi':lstfwi,'ray':ray,'lstR':lstR}
    return render(request,"stationvisio.html",context)


def home(request):
    # print("date",str((datetime.datetime.now())))
    # print("date2", str((datetime.datetime.now()).strftime("%M")))
    tab=CapSol.objects.last()
    cap1_last_data = CapSol2.objects.filter(devId="1").latest('dt')
    cap2_last_data = CapSol2.objects.filter(devId="2").latest('dt')
    cap3_last_data = CapSol2.objects.filter(devId="3").latest('dt')
    cap4_last_data = CapSol2.objects.filter(devId="4").latest('dt')
    cap2 = CapSol2.objects.last()

    bv= batvanne.objects.last()
    # print("last",str((tab.time)))

    f = CapSol.objects.first()
    tab2=CapSol.objects.all()

    max_temp=CapSol.objects.all().aggregate(Max('Temp'))
    min_temp = CapSol.objects.all().aggregate(Min('Temp'))
    moy=(max_temp["Temp__max"]+min_temp["Temp__min"])/2
    print((max_temp["Temp__max"]+min_temp["Temp__min"])/2)

    context = {'tab': tab,'tab2':tab2,'max_temp':max_temp,'min_temp':min_temp,'moy':moy,'f':f,'cap1_last_data':cap1_last_data,'cap2_last_data':cap2_last_data,
    'cap3_last_data':cap3_last_data, 'cap4_last_data':cap4_last_data}

    #tab2 = CapSol.objects.last().filter(devId='03')
    if (request.method == "POST"):
        if (request.POST.get('btn1', False)) == 'two':
            new_value_button = vann(onoff=request.POST.get(
                'btn1'))
            print(request.POST.get('btn1', False))
            new_value_button.save()
            x=vann.objects.create(onoff=False)
            print("x :", x)
            return HttpResponseRedirect('/')

        if (request.POST.get('btn', True)) == 'two':
            new_value_button1 = vann(onoff=request.POST.get(
                'btn'))
            print(request.POST.get('btn', True))
            new_value_button1.save()

            w=vann.objects.create(onoff=True)
            print("w :", w)
            return HttpResponseRedirect('/')

        elif request.POST.get('startdate') == 'one':
            fromdate = request.POST.get('startdate')
            # print(type(datetime.datetime.now()))
            print("fromdate")
            print(fromdate)
            client1 = mqtt.Client()

            client1.connect("broker.hivemq.com", 1883, 80)
            client1.publish("time", str(fromdate))

            return HttpResponseRedirect('/')

    # if (request.method == "POST"):
    #     fromdate = request.POST.get('startdate')
    #     # print(type(datetime.datetime.now()))
    #     print("fromdate" , fromdate)

    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    date_from2 = datetime.datetime.now() - datetime.timedelta(days=7)
    date_from3 = datetime.datetime.now() - datetime.timedelta(days=14)
    date_from4 = datetime.datetime.now() - datetime.timedelta(days=30)
    created_documents = CapSol.objects.filter(dt__gte=date_from)

    created_documents2 = CapSol.objects.filter(dt__gte=date_from2).count()
    created_documents3 = CapSol.objects.filter(dt__gte=date_from3).count()
    created_documents4 = CapSol.objects.filter(dt__gte=date_from4).count()

    now = (datetime.datetime.now()).strftime("%M")
    x = CapSol.objects.filter(time__minute=now).count()
    # print("x", str(x))
    labels = []
    dataa = []
    dataa2 = []
    alla = CapSol.objects.all()
    for data in alla:
        labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
        dataa.append(data.Temp)
        dataa2.append(data.Hum)
        # print("labels0",labels)

    # print("labelall",labels)
    if (request.method == "POST"):
        labels.clear()
        dataa.clear()
        dataa2.clear()

        fromdate = request.POST.get('startdate')
        # print(type(datetime.datetime.now()))
        print("fromdate")
        print(fromdate)
        # todate = request.POST.get('enddate')
        # print("todate")
        # print(todate)
        # first = CapSol.objects.first()
        # print("first date", str(first.dt))
        # lastdate = CapSol.objects.last()
        # print("last date", str(lastdate.dt))
        # if fromdate != "" and todate != "":
        #     # to = datetime.datetime.strptime(todate, '%Y-%m-%d')+datetime.timedelta(days=1)
        #     to = datetime.datetime.strptime(todate, '%Y-%m-%d') + datetime.timedelta(days=1)
        #     # fromdate = datetime.datetime("07-07")
        #     created_documents5 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('dt')
        #     print("created_documents5",created_documents5)
        #     for data in created_documents5:
        #         labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
        #         dataa.append(data.Temp)
        #         dataa2.append(data.Hum)
        #
        # if fromdate =="":
        #     fromdate= first.dt
        #
        # if todate == "":
        #     to = (lastdate.dt)+ datetime.timedelta(days=1)
        #     todate = to + datetime.timedelta(days=1)
        #     labels.clear()
        #     dataa.clear()
        #     dataa2.clear()
        #     created_documents6 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('id')
        #     # print("created_documents6",created_documents6)
        #
        #     for data in created_documents6:
        #
        #         labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
        #         dataa.append(data.Temp)
        #         dataa2.append(data.Hum)

    context = {'tab': tab,'tab2':tab2,'max_temp':max_temp,'min_temp':min_temp,'moy':moy,'f':f,'labels':labels,'dataa':dataa,'dataa2':dataa2,'cap2':cap2, 'bv':bv,'cap1_last_data':cap1_last_data,'cap2_last_data':cap2_last_data,
    'cap3_last_data':cap3_last_data, 'cap4_last_data':cap4_last_data}
    return render(request, "index.html", context)


    # completed = request.POST('checks')
    # print(completed)
    # if 'checks' in request.GET:

    # toSave = vanne.objects.all()
    # geek_object = vanne.objects.create(onoff=True)
    # geek_object.save()
    # toSave.save()
    # print(toSave)
def fetch_data_for_eto():
    # Période de données : hier de 00:00 à aujourd’hui 00:00
    start_of_yesterday = (timezone.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_today = start_of_yesterday + timedelta(days=1)

    # Moyennes des autres paramètres (hors Ray)
    weather_data = Data2.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).aggregate(
        Avg('Temp'),
        Avg('Hum'),
        Avg('Wind_Speed'),
        Avg('Pr')
    )

    # Min/max température et humidité
    temp_max = Data2.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).order_by('-Temp').first().Temp
    temp_min = Data2.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).order_by('Temp').first().Temp
    hum_max = Data2.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).order_by('-Hum').first().Hum
    hum_min = Data2.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).order_by('Hum').first().Hum

    temp_avg = weather_data['Temp__avg']
    wind_speed_avg = round(weather_data['Wind_Speed__avg'] / 3.6, 2) if weather_data['Wind_Speed__avg'] else 0

    # Moyenne horaire de Ray (24 intervalles horaires)
    hourly_ray_averages = []
    for hour in range(24):
        interval_start = start_of_yesterday + timedelta(hours=hour)
        interval_end = interval_start + timedelta(hours=1)
        avg_ray = Ray2.objects.filter(DateRay__range=(interval_start, interval_end)).aggregate(avg=Avg('Ray'))['avg']
        if avg_ray is not None:
            hourly_ray_averages.append(avg_ray)

    # Moyenne journalière sur les 24 heures
    if hourly_ray_averages:
        daily_ray_avg = sum(hourly_ray_averages) / len(hourly_ray_averages)
    else:
        daily_ray_avg = 0

    # Conversion en MJ/m²
    radiation_sum = daily_ray_avg * 0.0864

    # Numéro du jour dans l’année (pour hier)
    day_of_year = start_of_yesterday.timetuple().tm_yday

    return {
        'altitude': 532,
        'latitude': 33.51,
        'day_of_year': day_of_year,
        'pressure': weather_data['Pr__avg'],
        'humidity_max': hum_max,
        'humidity_min': hum_min,
        'temp_avg': temp_avg,
        'temp_max': temp_max,
        'temp_min': temp_min,
        'radiation_sum': radiation_sum,
        'wind_speed_avg': wind_speed_avg
    }
def fetch_data_for_etoDR():
    # Début et fin de la journée d'hier
    start_of_yesterday = (timezone.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_today = start_of_yesterday + timedelta(days=1)

    # Moyennes globales (hors illumination)
    weather_data = wsd.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).aggregate(
        Avg('TEM'),
        Avg('HUM'),
        Avg('wind_speed')
    )
    weather_data1 = Data2.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).aggregate(
        Avg('Pr')
    )

    # Température et humidité min/max
    temp_max = wsd.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).order_by('-TEM').first().TEM
    temp_min = wsd.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).order_by('TEM').first().TEM
    hum_max = wsd.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).order_by('-HUM').first().HUM
    hum_min = wsd.objects.filter(Time_Stamp__range=(start_of_yesterday, start_of_today)).order_by('HUM').first().HUM

    # Calcul des 24 moyennes horaires d'illumination
    hourly_illum_averages = []
    for hour in range(24):
        interval_start = start_of_yesterday + timedelta(hours=hour)
        interval_end = interval_start + timedelta(hours=1)
        avg_illum = wsd.objects.filter(Time_Stamp__range=(interval_start, interval_end)).aggregate(avg=Avg('illumination'))['avg']
        if avg_illum is not None:
            hourly_illum_averages.append(avg_illum)

    # Moyenne des 24 moyennes horaires
    if hourly_illum_averages:
        daily_illum_avg = sum(hourly_illum_averages) / len(hourly_illum_averages)
    else:
        daily_illum_avg = 0

    # Conversion en MJ/m²
    radiation_sum = daily_illum_avg * 0.0864

    wind_speed_avg = round(weather_data['wind_speed__avg'] / 3.6, 2) if weather_data['wind_speed__avg'] else 0

    # Numéro du jour dans l’année pour hier
    day_of_year = start_of_yesterday.timetuple().tm_yday

    return {
        'altitude': 532,
        'latitude': 33.51,
        'day_of_year': day_of_year,
        'pressure': weather_data1['Pr__avg'],
        'humidity_max': hum_max,
        'humidity_min': hum_min,
        'temp_avg': weather_data['TEM__avg'],
        'temp_max': temp_max,
        'temp_min': temp_min,
        'radiation_sum': radiation_sum,
        'wind_speed_avg': wind_speed_avg
    }
def ETODR():
    data = fetch_data_for_etoDR()

    A6 = data['altitude']  # Altitude (m)
    B6 = data['latitude']  # Latitude (degrés)
    C6 = 2  # Hauteur de l'anémomètre (m)
    D11 = data['day_of_year']  # Jour de l'année
    E6 = data['pressure']  # Pression moyenne (hPa)
    F11 = data['humidity_max']  # Humidité max (%)
    G11 = data['humidity_min']  # Humidité min (%)
    H11 = data['temp_avg']  # Température moyenne (°C)
    I11 = data['temp_max']  # Température max (°C)
    J11 = data['temp_min']  # Température min (°C)
    K11 = data['radiation_sum']  # Radiation solaire (MJ/m²)
    L11 = data['wind_speed_avg']  # Vitesse moyenne du vent (m/s)

    # Remplacement des None par une valeur par défaut (ex: 0 ou une moyenne raisonnable)
    # I11 = I11 if I11 is not None else 0
    # J11 = J11 if J11 is not None else 0
    # H11 = H11 if H11 is not None else (I11 + J11) / 2
    # F11 = F11 if F11 is not None else 0
    # G11 = G11 if G11 is not None else 0
    # E6 = E6 if E6 is not None else 1013  # Pression atmosphérique standard

    # Calculs
    P = 1013 * ((293 - 0.0065 * A6) / 293) ** 5.256
    λ = 694.5 * (1 - 0.000946 * H11)
    γ = 0.2805555 * E6 / (0.622 * λ)
    U2 = 4.868 * L11 / np.log(67.75 * C6 - 5.42)
    γ_prime = γ * (1 + 0.34 * U2)

    if np.isnan(H11):
        ea_Tmoy = 6.108 * np.exp((17.27 * (I11 + J11) / 2) / ((I11 + J11) / 2 + 237.3))
    else:
        ea_Tmoy = 6.108 * np.exp((17.27 * H11) / (H11 + 237.3))

    if pd.isna(F11) or pd.isna(I11):
        ed = ea_Tmoy * E6 / 100
    else:
        ed = (6.108 * np.exp((17.27 * J11) / (J11 + 237.3)) * F11 +
              6.108 * np.exp((17.27 * I11) / (I11 + 237.3)) * G11) / 200

    Δ = 4098.171 * ea_Tmoy / (ea_Tmoy + 237.3) ** 2
    dr = 1 + 0.033 * np.cos(2 * np.pi * D11 / 365)
    δ = 0.4093 * np.sin(2 * np.pi * (284 + D11) / 365)
    ωs = np.arccos(-np.tan(np.radians(B6)) * np.tan(δ))
    Rsmm = K11 / λ
    Ra = (24 / np.pi) * 1367 * dr * (ωs * np.sin(np.radians(B6)) * np.sin(δ) +
                                     np.cos(np.radians(B6)) * np.cos(δ) * np.sin(ωs))
    Ramm = Ra / λ
    Rso = (0.75 + 2 * (10 ** -5) * A6) * Ramm

    if pd.isna(F11) or pd.isna(I11):
        Rn = 0.77 * Rsmm - (1.35 * (Rsmm / Rso) - 0.35) * (0.34 - 0.14 * np.sqrt(ed)) * (1360.8 * (10 ** -9) / λ) * (H11 + 273.16) ** 4
    else:
        Rn = (0.77 * Rsmm - (1.35 * (Rsmm / Rso) - 0.35) * (0.34 - 0.14 * np.sqrt(ed)) * (1360.8 * (10 ** -9) / λ) *
              ((I11 + 273.16) ** 4 + (J11 + 273.16) ** 4) / 2)

    ETrad = (Δ * Rn) / (Δ + γ_prime)

    if np.isnan(H11):
        ETaero = (γ * (90 / ((I11 + J11) / 2 + 273.16)) * U2 * (ea_Tmoy - ed)) / (Δ + γ_prime)
    else:
        ETaero = (γ * (90 / (H11 + 273.16)) * U2 * (ea_Tmoy - ed)) / (Δ + γ_prime)

    ETo = ETrad + ETaero

    # Résultats
    print(f"ETo: {ETo} mm/jour")

    # Enregistrement dans la base de données
    ET0DR.objects.create(
        value=round(ETo, 2),
        WSavg=L11,
        Tmax=I11,
        Tmin=J11,
        Tavg=H11,
        Hmax=F11,
        Hmin=G11,
        Raym=round(K11, 2),
        U2=U2,
        Delta=D11
    )

def ETO():
    data = fetch_data_for_eto()

    A6 = data['altitude']  # Altitude (m)
    B6 = data['latitude']  # Latitude (degrés)
    C6 = 2  # Hauteur de l'anémomètre (m)
    D11 = data['day_of_year']  # Jour de l'année
    E6 = data['pressure']  # Pression moyenne (hPa)
    F11 = data['humidity_max']  # Humidité max (%)
    G11 = data['humidity_min']  # Humidité min (%)
    H11 = data['temp_avg']  # Température moyenne (°C)
    I11 = data['temp_max']  # Température max (°C)
    J11 = data['temp_min']  # Température min (°C)
    K11 = data['radiation_sum']  # Radiation solaire (MJ/m²)
    L11 = data['wind_speed_avg']  # Vitesse moyenne du vent (m/s)

    # Calculs
    P = 1013 * ((293 - 0.0065 * A6) / 293) ** 5.256
    λ = 694.5 * (1 - 0.000946 * H11)
    γ = 0.2805555 * E6 / (0.622 * λ)
    U2 = 4.868 * L11 / np.log(67.75 * C6 - 5.42)
    γ_prime = γ * (1 + 0.34 * U2)

    if np.isnan(H11):
        ea_Tmoy = 6.108 * np.exp((17.27 * (I11 + J11) / 2) / ((I11 + J11) / 2 + 237.3))
    else:
        ea_Tmoy = 6.108 * np.exp((17.27 * H11) / (H11 + 237.3))

    if pd.isna(F11) or pd.isna(I11):
        ed = ea_Tmoy * E6 / 100
    else:
        ed = (6.108 * np.exp((17.27 * J11) / (J11 + 237.3)) * F11 +
              6.108 * np.exp((17.27 * I11) / (I11 + 237.3)) * G11) / 200

    Δ = 4098.171 * ea_Tmoy / (ea_Tmoy + 237.3) ** 2
    dr = 1 + 0.033 * np.cos(2 * np.pi * D11 / 365)
    δ = 0.4093 * np.sin(2 * np.pi * (284 + D11) / 365)
    ωs = np.arccos(-np.tan(np.radians(B6)) * np.tan(δ))
    Rsmm = K11 / λ
    Ra = (24 / np.pi) * 1367 * dr * (ωs * np.sin(np.radians(B6)) * np.sin(δ) +
                                     np.cos(np.radians(B6)) * np.cos(δ) * np.sin(ωs))
    Ramm = Ra / λ
    Rso = (0.75 + 2 * (10 ** -5) * A6) * Ramm

    if pd.isna(F11) or pd.isna(I11):
        Rn = 0.77 * Rsmm - (1.35 * (Rsmm / Rso) - 0.35) * (0.34 - 0.14 * np.sqrt(ed)) * (1360.8 * (10 ** -9) / λ) * (H11 + 273.16) ** 4
    else:
        Rn = (0.77 * Rsmm - (1.35 * (Rsmm / Rso) - 0.35) * (0.34 - 0.14 * np.sqrt(ed)) * (1360.8 * (10 ** -9) / λ) *
              ((I11 + 273.16) ** 4 + (J11 + 273.16) ** 4) / 2)

    ETrad = (Δ * Rn) / (Δ + γ_prime)

    if np.isnan(H11):
        ETaero = (γ * (90 / ((I11 + J11) / 2 + 273.16)) * U2 * (ea_Tmoy - ed)) / (Δ + γ_prime)
    else:
        ETaero = (γ * (90 / (H11 + 273.16)) * U2 * (ea_Tmoy - ed)) / (Δ + γ_prime)

    ETo = ETrad + ETaero

    # Résultats
    print(f"ETo: {ETo} mm/jour")

    # Enregistrement dans la base de données
    ET0o.objects.create(
        value=round(ETo,2),
        WSavg=L11,
        Tmax=I11,
        Tmin=J11,
        Tavg=H11,
        Hmax=F11,
        Hmin=G11,
        Raym=round(K11, 2),
        U2=U2,
        Delta=D11
    )

#ETO()

# def run_eto_once_per_day():
#     current_date = now().date()
#     current_time = now()

#     print(f"Vérification à {current_time}...")

#     # Vérifier si ET0 a été calculé aujourd'hui
#     already_executed = ET0ExecutionLog.objects.filter(date=current_date).exists()

#     if not already_executed and current_time.hour == 1:
#         # Exécuter ET0 et enregistrer l'exécution
#         ETO()
#         print("✅ ET0 calculé et enregistré.")

#         # Sauvegarde de l'exécution
#         ET0ExecutionLog.objects.create(date=current_date)
#     else:
#         print("⏳ ET0 a déjà été calculé aujourd'hui ou il n'est pas encore temps.")
from django.utils.timezone import now as dj_now

def et0_job(request):
    current_time = dj_now()  # Utilisation de la gestion des fuseaux horaires Django
    current_date = current_time.date()

    print(f"📅 Date actuelle : {current_date}")
    print(f"⏳ Heure actuelle : {current_time.time()}")

    # Vérifier si ET0 a déjà été calculé aujourd'hui
    last_eto_entry = ET0o.objects.filter(Time_Stamp__date=current_date).last()
    last_eto_entry1 = ET0DR.objects.filter(Time_Stamp__date=current_date).last()

    print(f"🔍 Dernière entrée ET0 : {last_eto_entry}")
    print(f"🔍 Dernière entrée ET0 Dragino : {last_eto_entry1}")

    # Vérifier si on est entre 1h et 2h du matin
    if 0 <= current_time.hour < 1:
        if not last_eto_entry and not last_eto_entry1:
            print("🚀 Calcul simultané de ET0 et ET0 Dragino...")
            ETO()
            ETODR()
            print(f"✅ ET0 et ET0 Dragino calculés et enregistrés à {current_time}")
        else:
            if last_eto_entry:
                print(f"⚠️ ET0 déjà calculé aujourd'hui à : {last_eto_entry.Time_Stamp}")
            else:
                print("✅ Calcul de ET0...")
                ETO()

            if last_eto_entry1:
                print(f"⚠️ ET0 Dragino déjà calculé aujourd'hui à : {last_eto_entry1.Time_Stamp}")
            else:
                print("✅ Calcul de ET0 Dragino...")
                ETODR()
    else:
        print("⏳ Il n'est pas encore temps de calculer ET0 (attendre entre 1h et 2h du matin).")

    return render(request, "job.html", {})
from django.utils import timezone
import pytz

def wsopen(request):
    maroc_tz = pytz.timezone('Africa/Casablanca')
    now = timezone.now().astimezone(maroc_tz).replace(hour=0, minute=0, second=0, microsecond=0)
    print("La date aujourd'hui est ", now)

    current_time = timezone.now().astimezone(maroc_tz)
    current_date = current_time.date()  # Date actuelle sans l'heure
    print("Le temps de comparaison : ", current_time)

    # Récupération des données à partir de minuit
    hm = Data2.objects.filter(Time_Stamp__gte=now)
    hm1 = Ray2.objects.filter(DateRay__gte=now)
    # send_simple_message()
    # Calcul des valeurs max et min
    Tmmax = hm.aggregate(Max('Temp'))['Temp__max'] or 0
    Tmmin = hm.aggregate(Min('Temp'))['Temp__min'] or 0
    Hx = hm.aggregate(Max('Hum'))['Hum__max'] or 0
    Hm = hm.aggregate(Min('Hum'))['Hum__min'] or 0
    Sx = hm.aggregate(Max('Wind_Speed'))['Wind_Speed__max'] or 0
    Sm = hm.aggregate(Min('Wind_Speed'))['Wind_Speed__min'] or 0
    Rx = hm1.aggregate(Max('Ray'))['Ray__max'] or 0
    Rm = hm1.aggregate(Min('Ray'))['Ray__min'] or 0
    Tmavg = hm.aggregate(Avg('Temp'))['Temp__avg'] or 0
    Havg = hm.aggregate(Avg('Hum'))['Hum__avg'] or 0
    Savg = hm.aggregate(Avg('Wind_Speed'))['Wind_Speed__avg'] or 0
    Ravg = hm1.aggregate(Avg('Ray'))['Ray__avg'] or 0

    # Fonction pour récupérer les précipitations sur une période donnée
    def get_rain_sum(start_time):
        return Data2.objects.filter(Time_Stamp__gte=start_time, Time_Stamp__lte=current_time).aggregate(Sum('Rain'))['Rain__sum'] or 0

    one_hour_ago = current_time - timezone.timedelta(hours=1)
    eight_hours_ago = current_time - timezone.timedelta(hours=8)
    one_day_ago = current_time - timezone.timedelta(days=1)
    one_week_ago = current_time - timezone.timedelta(days=7)

    p1h = round(get_rain_sum(one_hour_ago), 2)
    p8h = round(get_rain_sum(eight_hours_ago), 2)
    p24h = round(get_rain_sum(one_day_ago), 2)
    p1w = round(get_rain_sum(one_week_ago), 2)

    tab = Data2.objects.last()
    tab2 = Ray2.objects.last()
    eto = ET0o.objects.last()
    lstfwi = DataFwiO.objects.last()

    context = {
    'tab': tab, 'tab2': tab2, 'eto': eto, 'p1w': p1w, 'p24h': p24h, 'p8h': p8h, 'p1h': p1h,
    'Rx': Rx, 'Rm': Rm, 'Sx': Sx, 'Sm': Sm, 'Hx': Hx, 'Hm': Hm, 'Tmmax': Tmmax, 'Tmmin': Tmmin,
    'Tmavg': round(Tmavg, 2), 'Havg': round(Havg, 2), 'Savg': round(Savg, 2), 'Ravg': round(Ravg, 2),
    'lstfwi': lstfwi
    }
    return render(request, "ws_open.html", context)


def wsopen1(request):
    now = (datetime.datetime.now()).replace(hour=0, minute=0, second=0, microsecond=0)
    print(now)
    current_time = datetime.datetime.now()
    current_date = current_time.date()
    print(current_time)

    # last_eto_entry = ET0o.objects.filter(Time_Stamp__date=current_date).last()

    # if current_time.hour == 1 and not last_eto_entry:
    #     ETO()
    #     print("ET0 calculé et enregistré.")
    # else:
    #     print("ET0 a déjà été calculé aujourd'hui ou il n'est pas encore temps.")

    hm = wsd.objects.filter(Time_Stamp__gte=now)
    lstfwi = DataFwiO.objects.last()
    # ETODR()
    """ Température """
    Tmmax = hm.aggregate(Max('TEM'))['TEM__max']
    Tmmin = hm.aggregate(Min('TEM'))['TEM__min']
    Tmavg = hm.aggregate(Avg('TEM'))['TEM__avg'] or 0

    """ Humidité """
    Hx = hm.aggregate(Max('HUM'))['HUM__max']
    Hm = hm.aggregate(Min('HUM'))['HUM__min']
    Havg = hm.aggregate(Avg('HUM'))['HUM__avg'] or 0

    """ Vitesse du vent """
    Sx = hm.aggregate(Max('wind_speed'))['wind_speed__max']
    Sm = hm.aggregate(Min('wind_speed'))['wind_speed__min']
    Savg = hm.aggregate(Avg('wind_speed'))['wind_speed__avg'] or 0

    """ Illumination """
    Rx = hm.aggregate(Max('illumination'))['illumination__max']
    Rm = hm.aggregate(Min('illumination'))['illumination__min']
    Ravg = hm.aggregate(Avg('illumination'))['illumination__avg'] or 0

    """ Pluie """
    one_hour = current_time - datetime.timedelta(hours=1)
    huit_hour = current_time - datetime.timedelta(hours=8)
    one_day = current_time - datetime.timedelta(days=1)
    week = current_time - datetime.timedelta(days=7)

    posts = wsd.objects.filter(Time_Stamp__gte=one_hour, Time_Stamp__lte=current_time)
    post8 = wsd.objects.filter(Time_Stamp__gte=huit_hour, Time_Stamp__lte=current_time)
    post24 = wsd.objects.filter(Time_Stamp__gte=one_day, Time_Stamp__lte=current_time)
    postweek = wsd.objects.filter(Time_Stamp__gte=week, Time_Stamp__lte=current_time)

    def get_rain_sum(queryset):
        rain_sum = queryset.aggregate(Sum('rain_gauge'))['rain_gauge__sum']
        return round(rain_sum, 2) if rain_sum is not None else 0

    p1h = get_rain_sum(posts)
    p8h = get_rain_sum(post8)
    p24h = get_rain_sum(post24)
    p1w = get_rain_sum(postweek)

    tab = wsd.objects.last()
    eto = ET0o.objects.last()
    last_et0dr = ET0DR.objects.last()
    context = {
    'tab': tab, 'eto': eto, 'p1w': p1w, 'p24h': p24h, 'p8h': p8h, 'p1h': p1h,
    'Rx': Rx, 'Rm': Rm, 'Ravg': round(Ravg, 2),
    'Sx': Sx, 'Sm': Sm, 'Savg': round(Savg, 2),
    'Hx': Hx, 'Hm': Hm, 'Havg': round(Havg, 2),
    'Tmmax': Tmmax, 'Tmmin': Tmmin, 'Tmavg': round(Tmavg, 2),
    'lstfwi': lstfwi, 'last_et0dr': last_et0dr
    }

    return render(request, "ws_open1.html", context)

# def test0(request):
#     one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
#     labels = []
#     dataa = []
#     all = Ws.objects.all()
#     # print("all", all)
#     for i in all:
#         labels.append((i.date).strftime("%Y-%m-%d %H:%M:%S"))
#         # print("labels", labels)
#         dataa.append(i.Temperature)
#     lst = Ws.objects.last()
#     context={'all':all,'lst':lst,'labels':labels,'dataa':dataa}
#     return render(request,"test.html",context)

# def test0(request):
#     return render(request,"test.html")
def cwsi_data(request):
    # Retrieve all records from the cwsi model
    cwsi_records = cwsi.objects.all()
    cw = cwsiO.objects.all()
    # Pass the data to the template
    context = {
        'cwsi_records': cwsi_records,
        'cw' : cw
    }
    return render(request, 'cwsi/cwsi01.html', context)

def ET0o_calc():

    # exemple()

    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0,
                                                                                 microsecond=0)
    now = (datetime.datetime.now()).replace(hour=0, minute=0, second=0, microsecond=0)
    onedayRay = one_day_ago.replace(hour=7)
    todayRay = one_day_ago.replace(hour=20)
    posts = Data.objects.filter(Time_Stamp__gte=one_day_ago, Time_Stamp__lte=now)
    # print("posts ws", posts.count())
    print("heure", one_day_ago)
    print("to heure", todayRay)

    post = Data.objects.filter(Time_Stamp__gte=one_day_ago, Time_Stamp__lte=now)
    rav = post.count()
    print("nbrs ray1", rav)
    print("____________________________________filtre par heure _______________________________________")

    filtresup = Data.objects.filter(Time_Stamp__gte=onedayRay, Time_Stamp__lte=todayRay)
    print("filtre nbr:", filtresup.count())
    w = post.aggregate(Avg('Ray'))
    print("moy ray :", w)
    lit = list(w.items())
    rayonnement = lit[0][1]
    print("avreage ray :", rayonnement)
    print("_____________________________________fin filtre par heure __________________________________")

    """ wind speed opensnz"""
    # wind_s = Ws.objects.filter(date__gte=one_day_ago, date__lte=now)
    # wind_avg= wind_s.aggregate(Avg('Vent'))
    # print(wind_avg)
    # dicttolistVent = list(wind_avg.items())
    # avgvent = (round(dicttolistVent[0][1] / 3.6, 4))
    # print(avgvent)
    # wind_sp = wind_s.aggregate(Max('Vent'))
    # spw = list(wind_sp.items())
    # sw = float(spw[0][1])
    # print("speed max visio :", sw)

    wsp = Data.objects.filter(Time_Stamp__gte=onedayRay, Time_Stamp__lte=todayRay)
    awsp = wsp.aggregate(Sum('Wind_Speed'))
    listws = list(awsp.items())
    avgws = round(listws[0][1]/rav,4)
    print("avrege open snz vent :", avgws)
    # dif_ws=avgws-avgvent
    # print("difference vent :", dif_ws)
    totalRay = post.values('Ray').aggregate(Sum('Ray'))
    Maxtemp = posts.values('Temp').aggregate(Max('Temp'))
    Mintemp = posts.values('Temp').aggregate(Min('Temp'))
    MaxHum = posts.values('Hum').aggregate(Max('Hum'))
    MinHum = posts.values('Hum').aggregate(Min('Hum'))
    avreage = posts.aggregate(Avg('Wind_Speed'))

    dicttolistVent = list(avreage.items())
    avgvent = (round(dicttolistVent[0][1] / 3.6, 4))
    vitvent = round(dicttolistVent[0][1], 4)
    print("vitvent :", vitvent)
    dicttolisTmax = list(Maxtemp.items())
    Tmmax = dicttolisTmax[0][1]
    dicttolisTmin = list(Mintemp.items())
    Tmmin = dicttolisTmin[0][1]
    dicttolisHmax = list(MaxHum.items())
    Hmax = dicttolisHmax[0][1]
    dicttolisHmin = list(MinHum.items())
    Hmin = dicttolisHmin[0][1]
    # print("posts", posts)
    print("tv", avgvent)
    print("tr", totalRay)
    print("tmin", Tmmin)
    print("tmax", Tmmax)
    print("hmin", Hmin)
    print("hmax", Hmax)
    print("avg :", avgvent)
    B2 =one_day_ago.timetuple().tm_yday
    print("b2", B2)

    RS = 7875  # totl radiation
    Tmin = Tmmin
    Tmax = Tmmax
    HRmin = Hmin
    HRmax = Hmax
    u = avgws  # m/s moyen
    print("--------------------------------------------------------------")
    station = pm.Station(latitude=33.01, altitude=640)
    station.anemometer_height = 2
    r = round(rayonnement * 0.0864, 2)
    print(r)

    day = station.day_entry(B2,
                            temp_min=Tmmin,
                            temp_max=Tmmax,
                            wind_speed=u,
                            humidity_max=HRmax,
                            humidity_min= HRmin,
                            # humidity_mean=(Hmin + Hmax) * 0.5,
                            radiation_s=r,
                            )
    print("ETo opensnz for this day is", day.eto())
    eto=day.eto()
    durée = eto /0.05

    print("time of irrig ................",round(durée))

    client = mqtt.Client()

    client.connect("broker.hivemq.com", 1883, 80)

    client.publish("et", round(durée))  # publish the message typed by the user
    # print(msg)
    client.disconnect(); #disconnect from server
    print("--------------------------------------------------------------")
    M = round(rayonnement, 2)  # radiation/h
    print("ray ", M)
    N = round(M * 3600 * 0.000001 * 24, 2)  # Rs [MJm-2d-1]
    print("N :", N)
    u2 = round(u * 4.87 / math.log(67.8 * 2 - 5.42), 3)
    print("u2 ;", u2)
    latitude = 60
    altitude = 800
    ctesolaire = 0.082
    StefanBolt = 0.000000004896
    p = 3.140
    g = 0.000665 * 101.3 * math.pow(((293 - 0.0065 * altitude) / 293), 5.26)
    conversion = latitude * 3.1416 / 180
    Y = 1 + 0.033 * math.cos((2 * p * B2) / 365)
    Z = 0.409 * math.sin((2 * p * B2 / 365) - 1.39)
    AA = math.acos(-math.tan(conversion) * math.tan(Z))
    AB = (24 * 60 / p) * ctesolaire * Y * (
            AA * math.sin(conversion) * math.sin(Z) + math.cos(conversion) * math.cos(Z) * math.sin(AA))
    AC = AB * (0.75 + 0.00002 * altitude)
    AD = 1.35 * (N / AC) - 0.35
    AE = (0.6108 * math.exp(17.27 * Tmin / (Tmin + 237.3)) + 0.6108 * math.exp(17.27 * Tmax / (Tmax + 237.3))) / 2
    AF = (HRmin * 0.6108 * math.exp(17.27 * Tmax / (Tmax + 237.3)) + HRmax * 0.6108 * math.exp(
        17.27 * Tmin / (Tmin + 237.3))) / (2 * 100)
    AG = StefanBolt * 0.5 * ((Tmin + 273) ** 4 + (Tmax + 273) ** 4) * (0.34 - 0.14 * math.sqrt(AF)) * AD
    AH = (1 - 0.23) * N - AG
    AI = 7
    AJ = 4098 * 0.6108 * math.exp(17.27 * 0.5 * (Tmin + Tmax) / (0.5 * (Tmin + Tmax) + 237.3)) / (
            0.5 * (Tmin + Tmax) + 237.3) ** 2
    ET_0 = (0.408 * AJ * (AH - AI) + (1600 * g / ((Tmin + Tmax) * 0.5 + 273)) * u2 * (AE - AF)) / (
            AJ + g * (1 + 0.38 * u2))
    print("aj :", AJ)

    ET = round(ET_0, 2)
    print("ET_0", ET)

    # ET0.objects.create(value=ET, WSavg=avgvent, Tmax=Tmax, Tmin=Tmin, Hmax=HRmax, Hmin=HRmin, Raym=M, U2=u2, Delta=B2)
    print("__________________________________ET_O Calculé________________________________")



# def pm():
#     import penmon as pm
#
#     ### create a station class with known location and elevation
#     from penmon import DayEntry
#
#     station = pm.Station(latitude=34.01, altitude=626)
#     station.anemometer_height = 2
#     r = 198.65 * 0.0864
#     print(r)
#
#     ### getting a day instance for August 16th
#     day = station.day_entry(301,
#                             temp_min=16.6,
#                             temp_max=30.95,
#                             wind_speed=1.86,
#                             humidity_mean=52.64,
#                             radiation_s=r,
#                             )
#     print("------------psychrometric_constant-----------")
#     print(day.psychrometric_constant())
#     print("-----------saturation_vapour_pressure------------")
#     print(day.saturation_vapour_pressure(30.95))
#     print("------------daylight_hours-----------")
#     print(day.daylight_hours())
#     print("----------latent_heat_of_vaporization-------------")
#
#     # print(day.sunshine_hours())
#     print(day.latent_heat_of_vaporization())
#     print("----------solar_radiation-------------")
#     print(day.solar_radiation())
#     print("------------R_ns-----------")
#     print(day.R_ns())
#     print("----------soil_heat_flux-------------")
#     print(day.soil_heat_flux())
#     print("-----------R_so------------")
#     print(day.R_so())
#     print("----------solar_radiation_in_mm-------------")
#     print(day.solar_radiation_in_mm())
#     print("-------------R_a_in_mm----------")
#     print(day.R_a_in_mm())
#     print("-------------R_a----------")
#     print(day.R_a())
#     print("-----------slope_of_saturation_vapour_pressure------------")
#     print(day.slope_of_saturation_vapour_pressure(30.65))
#     print("-----------------------")
#     day.radiation_s = r
#
#     print(day.temp_max)
#
#     print(day.wind_speed_2m())
#
#     print(" blot :", DayEntry.dew_point(self=day))
#     print("ETo for this day
#     is", day.eto())
def envfct(request):

    from django.db.models import Max, Min
import datetime

def envfct(request):
    # Obtenir le début de la journée actuelle
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Dernier enregistrement pour chaque capteur (S1, S2, S3)
    s1_last_data = Envdata.objects.filter(devId="S1").latest('Time_Stamp')
    s2_last_data = Envdata.objects.filter(devId="S2").latest('Time_Stamp')
    s3_last_data = Envdata.objects.filter(devId="S3").latest('Time_Stamp')

    # Dernier enregistrement pour wsd (si "TEM" est None, le remplacer par 0)
    last_wsd_data = wsd.objects.latest('Time_Stamp')
    last_wsd_value = last_wsd_data.TEM if last_wsd_data.TEM is not None else 0

    # Dernier enregistrement pour Data2 (si "Temp" est None, le remplacer par 0)
    last_data2 = Data2.objects.latest('Time_Stamp')
    last_data2_value = last_data2.Temp if last_data2.Temp is not None else 0

    context = {
        "s1_last_data": s1_last_data,
        "s2_last_data": s2_last_data,
        "s3_last_data": s3_last_data,
        "last_wsd_value": last_wsd_value,  # Ajouter la valeur de wsd
        "last_data2_value": last_data2_value,  # Ajouter la valeur de Data2
    }

    return render(request, "env1.html", context)




""" pm10"""
# For PM10
def pm10_data(request, days, template_name):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0,
                                                                                    microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.pm10)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.pm10)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.pm10)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, template_name, context)

def pm101(request):
    return pm10_data(request, 1, "enviro/pm101.html")

def pm103(request):
    return pm10_data(request, 3, "enviro/pm103.html")

def pm107(request):
    return pm10_data(request, 7, "enviro/pm107.html")

def pm1015(request):
    return pm10_data(request, 15, "enviro/pm1015.html")

""" fin pm10"""

"""pm1"""
# For PM
def pm_data(request, days, template_name):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0,
                                                                                    microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.pm)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.pm)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.pm)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, template_name, context)

def pm1(request):
    return pm_data(request, 1, "enviro/pm1.html")

def pm3(request):
    return pm_data(request, 3, "enviro/pm3.html")

def pm7(request):
    return pm_data(request, 7, "enviro/pm7.html")

def pm15(request):
    return pm_data(request, 15, "enviro/pm15.html")


""" fin pm1"""
"""pm25"""
# For PM2.5
def pm25_data(request, days, template_name):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0,
                                                                                    microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.pm25)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.pm25)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.pm25)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, template_name, context)

def pm251(request):
    return pm25_data(request, 1, "enviro/pm251.html")

def pm253(request):
    return pm25_data(request, 3, "enviro/pm253.html")

def pm257(request):
    return pm25_data(request, 7, "enviro/pm257.html")

def pm2515(request):
    return pm25_data(request, 15, "enviro/pm2515.html")

""" fin pm25"""

""" fin co2"""
# For CO2
def co2_data(request, days, template_name):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0,
                                                                                    microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.co2)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.co2)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.co2)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, template_name, context)

def co2v1(request):
    return co2_data(request, 1, "enviro/co21.html")

def co2v3(request):
    return co2_data(request, 3, "enviro/co23.html")

def co2v7(request):
    return co2_data(request, 7, "enviro/co27.html")

def co2v15(request):
    return co2_data(request, 15, "enviro/co215.html")

""" fin co2"""
""" ch2o"""
# For CH2O
def ch2o_data(request, days, template_name):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0,
                                                                                    microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.ch2o)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.ch2o)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.ch2o)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, template_name, context)

def ch2ov1(request):
    return ch2o_data(request, 1, "enviro/ch2o1.html")

def ch2ov3(request):
    return ch2o_data(request, 3, "enviro/ch2o3.html")

def ch2ov7(request):
    return ch2o_data(request, 7, "enviro/ch2o7.html")

def ch2ov15(request):
    return ch2o_data(request, 15, "enviro/ch2o15.html")

""" fin ch2o"""
# For o3
# For O3
def o3_data(request, days, template_name):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0,
                                                                                    microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.o3)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.o3)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.o3)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, template_name, context)

def o31(request):
    return o3_data(request, 1, "enviro/o31.html")

def o33(request):
    return o3_data(request, 3, "enviro/o33.html")

def o37(request):
    return o3_data(request, 7, "enviro/o37.html")

def o315(request):
    return o3_data(request, 15, "enviro/o315.html")


# For co
# For CO
def co_data(request, days, template_name):
    one_day_ago = (timezone.now() - datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0,
                                                                            microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        local_timestamp = localtime(i.Time_Stamp)
        timestamp_str = local_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        # timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.co)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.co)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.co)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, template_name, context)

def co1(request):
    return co_data(request, 1, "enviro/co1.html")

def co3(request):
    return co_data(request, 3, "enviro/co3.html")

def co7(request):
    return co_data(request, 7, "enviro/co7.html")

def co15(request):
    return co_data(request, 15, "enviro/co15.html")

# For TVOC
def tvoc_data(request, days, template_name):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0,
                                                                                    microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.tvoc)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.tvoc)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.tvoc)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, template_name, context)

def tvoc1(request):
    return tvoc_data(request, 1, "enviro/tvoc1.html")

def tvoc3(request):
    return tvoc_data(request, 3, "enviro/tvoc3.html")

def tvoc7(request):
    return tvoc_data(request, 7, "enviro/tvoc7.html")

def tvoc15(request):
    return tvoc_data(request, 15, "enviro/tvoc15.html")


# For no2
# For NO2
def no2_data(request, days, template_name):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0,
                                                                                    microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.no2)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.no2)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.no2)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, template_name, context)

def no21(request):
    return no2_data(request, 1, "enviro/no21.html")

def no23(request):
    return no2_data(request, 3, "enviro/no23.html")

def no27(request):
    return no2_data(request, 7, "enviro/no27.html")

def no215(request):
    return no2_data(request, 15, "enviro/no215.html")

#temp
# For temp
def tempv1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.temp)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.temp)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.temp)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, "enviro/temp1.html", context)


def tempv3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0, minute=0, second=0,
                                                                                microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(round(i.temp,2))
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(round(i.temp,2))
        else:
            labels2.append(timestamp_str)
            dataa2.append(round(i.temp,2))

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, "enviro/temp3.html", context)


def tempv7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0,
                                                                                microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.temp)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.temp)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.temp)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, "enviro/temp7.html", context)

def tempv15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0, minute=0, second=0,
                                                                                 microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.temp)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.temp)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.temp)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, "enviro/temp15.html", context)


# For hum
def humv1(request):
    one_day_ago = (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.hum)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.hum)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.hum)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, "enviro/hum1.html", context)

# Repeat a similar structure for humv3, humv7, and humv15 with the corresponding conditions.


def humv3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0, minute=0, second=0,
                                                                                microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.hum)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.hum)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.hum)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, "enviro/hum3.html", context)

# Repeat a similar structure for humv7 and humv15 with the corresponding conditions.


def humv7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0,
                                                                                microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.hum)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.hum)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.hum)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, "enviro/hum7.html", context)


def humv15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0, minute=0, second=0,
                                                                                 microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.hum)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.hum)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.hum)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, "enviro/hum15.html", context)


# For bat
def bat_data(request, days, template_name):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0,
                                                                                    microsecond=0)
    labels = []
    dataa = []
    labels1 = []
    dataa1 = []
    labels2 = []
    dataa2 = []

    all_data = Envdata.objects.filter(Time_Stamp__gte=one_day_ago)

    for i in all_data:
        timestamp_str = (i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S")
        if i.devId == "S1":
            labels.append(timestamp_str)
            dataa.append(i.bat)
        elif i.devId == "S2":
            labels1.append(timestamp_str)
            dataa1.append(i.bat)
        else:
            labels2.append(timestamp_str)
            dataa2.append(i.bat)

    last_data = Envdata.objects.last()

    context = {
        'all_data': all_data,
        'last_data': last_data,
        'labels': labels,
        'dataa': dataa,
        'labels1': labels1,
        'dataa1': dataa1,
        'labels2': labels2,
        'dataa2': dataa2,
    }

    return render(request, template_name, context)

def batv1(request):
    return bat_data(request, 1, "enviro/bat1.html")

def batv3(request):
    return bat_data(request, 3, "enviro/bat3.html")

def batv7(request):
    return bat_data(request, 7, "enviro/bat7.html")

def batv15(request):
    return bat_data(request, 15, "enviro/bat15.html")

@require_POST
@csrf_exempt
def v_chirpstack(request):
    print("**********************uplink")
    if 'event' in request.GET:
        event = str(request.GET['event'])
        if event == 'up' :
            print("*********************up")
            try :
                print("*************************try")
                data = json.loads(request.body)
                print(data)


                if data['deviceInfo']['devEui'] == WsSENSECAP_WeatherStation:
                    messages = data['object']['messages']
                    print("messages: ", messages)
                    batt_mesure = False
                    for mesage in messages:
                        for measurement in mesage:
                            print("lenght messages: ", len(messages))
                            if len(messages) >= 3 and not batt_mesure:
                                bat = measurement['Battery(%)']
                                batt_mesure = True
                                break
                            print(measurement['type'],measurement['measurementValue'])
                            if measurement['type'] =="Air Temperature":
                                airTemp = measurement['measurementValue']
                                continue
                            elif measurement['type'] =="Air Humidity":
                                airHum = measurement['measurementValue']
                                continue
                            elif measurement['type'] =="Light Intensity":
                                light = measurement['measurementValue']
                                continue
                            elif measurement['type'] =="UV Index":
                                uv = measurement['measurementValue']
                                continue
                            elif measurement['type'] =="Wind Speed":
                                windSpeed = measurement['measurementValue']
                                continue
                            elif measurement['type'] =="Wind Direction Sensor":
                                windDirection = measurement['measurementValue']
                                continue
                            elif measurement['type'] =="Rain Gauge":
                                rainfall = measurement['measurementValue']
                                continue
                            elif measurement['type'] =="Barometric Pressure":
                                pressure = measurement['measurementValue']
                                continue

                    object_WsSENSECAP = Data2()
                    object_WsSENSECAP.Temp = airTemp
                    # print(object_WsSENSECAP)
                    object_WsSENSECAP.Hum = airHum
                    object_WsSENSECAP.Wind_Speed = round((float(windSpeed)*3.6),4)
                    # object_WsSENSECAP.WindDirection = windDirection
                    object_WsSENSECAP.Rain = rainfall/4
                    # object_WsSENSECAP.Light = light
                    # object_WsSENSECAP.UV = uv
                    object_WsSENSECAP.Pr = pressure
                    # if batt_mesure:
                    #     object_WsSENSECAP.Bat = bat
                    # else:
                    #     object_WsSENSECAP_last_val_batt = WsSENSECAP.objects.last()
                    #     object_WsSENSECAP.Bat = object_WsSENSECAP_last_val_batt.Bat
                    object_WsSENSECAP.save()

                    # Vérifier si le devEui correspond au dispositif Model WSC1-L
                if data['deviceInfo']['devEui'] == 'a84041b02458e028':
                    print("Données reçues du dispositif Model WSC1-L")

                    # Récupération des données depuis 'object'
                    object_data = data.get('object', {})

                    # Création de l'objet `wsd`
                    object_wsd = wsd()

                    # Affectation des valeurs avec `get()` pour éviter les erreurs si une clé est absente
                    object_wsd.wind_direction_angle = object_data.get('wind_direction_angle', None)
                    object_wsd.wind_direction = object_data.get('wind_direction', None)
                    object_wsd.HUM = object_data.get('TEM', None)
                    object_wsd.rain_gauge = object_data.get('rain_gauge', None)
                    object_wsd.wind_speed = round((float(object_data.get('wind_speed', 0.0)) * 3.6), 4)  # Convertir en km/h
                    object_wsd.illumination = object_data.get('A1', None)
                    if object_wsd.illumination is not None:  # Vérifie que la valeur n'est pas None
                        object_wsd.illumination = round((float(object_wsd.illumination) * 0.8),2)  # Convertir et multiplier
                    object_wsd.TEM = object_data.get('HUM', None)


                    try:
                        # Sauvegarde dans la base de données
                        object_wsd.save()
                        print("Données enregistrées avec succès :", object_wsd)
                    except Exception as e:
                        print("Erreur lors de l'enregistrement :", e)
                else:
                    print("Dispositif non reconnu, données ignorées.")

                if data['deviceInfo']['devEui']==pyraGV:
                    input_mA: float = data['object']['IDC_intput_mA']
                    ray = 2000 * (1 + (input_mA - 20) / 16)
                    bat = data['object']['Bat_V']
                    db_obj = Ray2()
                    db_obj.Ray = round(ray,2)
                    db_obj.Bat = bat

                    try:
                        # Sauvegarde dans la base de données
                        db_obj.save()
                        print("Données enregistrées avec succès greeene vision :", db_obj)
                    except Exception as e:
                        print("Erreur lors de l'enregistrement :", e)
                else:
                    print("Dispositif non reconnu, données ignorées.")


                if data['deviceInfo']['devEui'] == 'a84041d10858e027':  # Vérifie si c'est bien le capteur de sol
                    print("📡 Données reçues du Capteur de sol")

                    # Récupération des données depuis 'object'
                    object_data = data.get('object', {})
                    batterie = object_data.get('Batterie', '0')  # Valeur par défaut '0' si absente

                    print("📊 object_data complet :", object_data)

                    # Boucle sur les capteurs de sol (Capteur_1 à Capteur_4)
                    for i in range(1, 5):
                        capteur_key = f"Capteur_{i}"
                        if capteur_key in object_data:
                            capteur_data = object_data[capteur_key]
                            print(f"🔎 {capteur_key} trouvé :", capteur_data)

                            try:
                                CapSol2.objects.create(
                                    devId=i,
                                    Temp=capteur_data.get('Temperature', '0'),
                                    Hum=capteur_data.get('Humidite', '0'),
                                    ec=capteur_data.get('Conductivite', '0'),
                                    N=capteur_data.get('Azote', '0'),
                                    P=capteur_data.get('Phosphore', '0'),
                                    K=capteur_data.get('Potassium', '0'),
                                    Sal=0,  # Valeur par défaut
                                    Bat=batterie
                                )
                                print(f"✅ Données enregistrées pour {capteur_key}: {capteur_data}")
                            except Exception as e:
                                print(f"❌ Erreur lors de l'enregistrement de {capteur_key}: {e}")

                if data['devEui'] == 'a84041d10858e027':
                    print("Données reçues du dispositif contenant plusieurs capteurs")

                    # Extraction des valeurs des capteurs
                    humidites = data.get("Humidite", [])
                    temperatures = data.get("Temperature", [])
                    conductivites = data.get("Conductivite", [])
                    azotes = data.get("Azote", [])
                    phosphores = data.get("Phosphore", [])
                    potassiums = data.get("Potassium", [])

                    # Vérifier que toutes les listes ont la même longueur (nombre de capteurs détectés)
                    capteur_count = min(len(humidites), len(temperatures), len(conductivites), len(azotes), len(phosphores), len(potassiums))

                    for i in range(capteur_count):
                        print(f"Traitement du capteur {i + 1}")

                        capteur = CapSol()
                        capteur.sensor_id = i + 1  # Numéro du capteur
                        capteur.Hum = humidites[i]
                        capteur.Temp = temperatures[i]
                        capteur.Ec = conductivites[i]
                        capteur.N = azotes[i]
                        capteur.P = phosphores[i]
                        capteur.K = potassiums[i]

                        try:
                            # Sauvegarde dans la base de données
                            capteur.save()
                            print(f"Données du capteur {i + 1} enregistrées avec succès :", capteur)
                        except Exception as e:
                            print(f"Erreur lors de l'enregistrement du capteur {i + 1} :", e)
                else:
                    print("Dispositif non reconnu, données ignorées.")



            except :
                print("chirpstack integration error")


    return HttpResponse(status=200)

# def cwsi_data(request):
#     # Retrieve all records from the cwsi model
#     cwsi_records = cwsi.objects.all()

#     # Pass the data to the template
#     context = {
#         'cwsi_records': cwsi_records
#     }
#     return render(request, 'cwsi/cwsi01.html', context)

from django.utils.timezone import make_aware
import datetime
from django.shortcuts import render
from .models import Data2, wsd  # Assurez-vous que ces modèles sont correctement importés

def filter_data(request, field_data2, field_wsd, template_name):
    """
    Fonction générique pour filtrer les données avec des champs différents pour Data2 et wsd.
    - field_data2 : Nom du champ à récupérer pour Data2 (ex : 'Temp', 'Hum', etc.).
    - field_wsd : Nom du champ à récupérer pour wsd (ex : 'TEM', 'HUM', etc.).
    - template_name : Nom du fichier HTML à rendre.
    """
    # Récupération des dates depuis le formulaire GET
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Si l'utilisateur a spécifié des dates, les convertir en datetime
    if start_date and end_date:
        start_date = make_aware(datetime.datetime.strptime(start_date, "%Y-%m-%d"))
        end_date = make_aware(datetime.datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59))
    else:
        # Sinon, récupérer les données de la dernière journée
        one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = make_aware(one_day_ago)
        end_date = make_aware(datetime.datetime.now().replace(hour=23, minute=59, second=59))

    # Filtrage des données dans la plage spécifiée
    all_data2 = Data2.objects.filter(Time_Stamp__range=(start_date, end_date))
    all_wsd = wsd.objects.filter(Time_Stamp__range=(start_date, end_date))
    print("Dta filter wsd : ",all_wsd,all_data2)
    # Extraction des données pour les graphiques
    labels_data2 = [data.Time_Stamp.strftime("%Y-%m-%d %H:%M:%S") for data in all_data2]
    labels_wsd = [data.Time_Stamp.strftime("%Y-%m-%d %H:%M:%S") for data in all_wsd]

    data_data2 = [getattr(data, field_data2, 0) if getattr(data, field_data2, None) is not None else 0 for data in all_data2]
    data_wsd = [getattr(data, field_wsd, 0) if getattr(data, field_wsd, None) is not None else 0 for data in all_wsd]
    print("Dta filter wsd : ",data_wsd,data_data2)
    # Récupération du dernier enregistrement (gestion des valeurs `None`)
    lst_data2 = Data2.objects.last()
    lst_wsd = wsd.objects.last()

    last_data2_value = getattr(lst_data2, field_data2, 0) if lst_data2 and getattr(lst_data2, field_data2, None) is not None else 0
    last_wsd_value = getattr(lst_wsd, field_wsd, 0) if lst_wsd and getattr(lst_wsd, field_wsd, None) is not None else 0
    zipped_data2 = zip(labels_data2, data_data2)
    zipped_datawsd = zip(labels_wsd, data_wsd)
    # Création du contexte
    context = {
        'all_data2': all_data2,
        'all_wsd': all_wsd,
        'lst_data2': last_data2_value,
        'lst_wsd': last_wsd_value,
        'labels_data2': labels_data2,
        'labels_wsd': labels_wsd,
        'data_data2': data_data2,
        'data_wsd': data_wsd,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d"),
        'zipped_data2': list(zipped_data2),
        'zipped_datawsd': list(zipped_datawsd),
    }

    return render(request, template_name, context)

# Vue pour la température
def data_filter(request):
    return filter_data(request, field_data2='Temp', field_wsd='TEM', template_name="enviro/temp1.html")

# Vue pour l'humidité
def data_filter_hum(request):
    return filter_data(request, field_data2='Hum', field_wsd='HUM', template_name="enviro/hum1.html")

# Vue pour la vitesse de vent
def data_filter_ws(request):
    return filter_data(request, field_data2='Wind_Speed', field_wsd='wind_speed', template_name="enviro/tvoc1.html")

# Vue pour la pluie
def data_filter_pl(request):
    return filter_data(request, field_data2='Rain', field_wsd='rain_gauge', template_name="enviro/tvoc3.html")

def data_filter_pl(request):
    return filter_data(request, field_data2='Rain', field_wsd='rain_gauge', template_name="enviro/tvoc3.html")

def data_filter_ry(request):
    # Récupération des valeurs du formulaire
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Initialisation des listes
    labels_data2 = []
    labels_wsd = []
    data_data2 = []
    data_wsd = []

    # Si l'utilisateur a spécifié des dates, on les utilise, sinon on prend la journée actuelle
    if start_date and end_date:
        # Conversion des chaînes de caractères en objets datetime
        start_date = make_aware(datetime.datetime.strptime(start_date, "%Y-%m-%d"))
        end_date = make_aware(datetime.datetime.strptime(end_date, "%Y-%m-%d"))

        # Ajout de la fin de journée (23:59:59) à la date de fin pour inclure toute la journée
        end_date = end_date.replace(hour=23, minute=59, second=59)

        # Filtrage des données entre la date de début et la date de fin pour les deux modèles
        all_data2 = Ray2.objects.filter(DateRay__range=(start_date, end_date))
        all_wsd = wsd.objects.filter(Time_Stamp__range=(start_date, end_date))

    else:
        # Si aucune date n'est spécifiée, on récupère les données de la journée en cours
        today = datetime.datetime.now()
        one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0,
                                                                                 microsecond=0)
        start_date = make_aware(datetime.datetime(today.year, today.month, today.day, 0, 0, 0))
        end_date = make_aware(datetime.datetime(today.year, today.month, today.day, 23, 59, 59))

        # Filtrage des données pour la journée actuelle
        all_data2 = Ray2.objects.filter(DateRay__gte=one_day_ago)
        all_wsd = wsd.objects.filter(Time_Stamp__gte=one_day_ago)

    # Collecte des labels et des données pour les graphiques (pour chaque classe)
    for data in all_data2:
        labels_data2.append(data.DateRay.strftime("%Y-%m-%d %H:%M:%S"))
        # Remplacement de None par 0
        data_data2.append(data.Ray if data.Ray is not None else 0)

    for data in all_wsd:
        labels_wsd.append(data.Time_Stamp.strftime("%Y-%m-%d %H:%M:%S"))
        # Remplacement de None par 0
        data_wsd.append(data.illumination if data.illumination is not None else 0)

    # Derniers objets de chaque modèle
    lst_data2 = Ray2.objects.last()
    lst_wsd = wsd.objects.last()

    # Création du contexte pour passer les données à la vue
    context = {
        'all_data2': all_data2,
        'all_wsd': all_wsd,
        'lst_data2': lst_data2,
        'lst_wsd': lst_wsd,
        'labels_data2': labels_data2,
        'labels_wsd': labels_wsd,
        'data_data2': data_data2,
        'data_wsd': data_wsd,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d"),
    }

    return render(request, "enviro/temp3.html", context)


def data_filter_et0(request):
    # Récupération des valeurs du formulaire
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Initialisation des listes
    labels_et0 = []
    labels_et0dr = []
    data_et0 = []
    data_et0dr = []

    # Si l'utilisateur a spécifié des dates, on les utilise, sinon on prend les 15 derniers jours
    if start_date and end_date:
        start_date = make_aware(datetime.datetime.strptime(start_date, "%Y-%m-%d"))
        end_date = make_aware(datetime.datetime.strptime(end_date, "%Y-%m-%d")).replace(hour=23, minute=59, second=59)
    else:
        start_date = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.datetime.now().replace(hour=23, minute=59, second=59)
        start_date = make_aware(start_date)
        end_date = make_aware(end_date)

    # Filtrage des données pour les classes ET0o et ET0DR
    all_et0 = ET0o.objects.filter(Time_Stamp__range=(start_date, end_date))
    all_et0dr = ET0DR.objects.filter(Time_Stamp__range=(start_date, end_date))

    # Collecte des labels et des données
    for data in all_et0:
        labels_et0.append(data.Time_Stamp.strftime("%Y-%m-%d"))
        data_et0.append(data.value if data.value is not None else 0)

    for data in all_et0dr:
        labels_et0dr.append(data.Time_Stamp.strftime("%Y-%m-%d"))
        data_et0dr.append(data.value if data.value is not None else 0)

    # Derniers objets de chaque modèle
    last_et0 = ET0o.objects.last()
    last_et0dr = ET0DR.objects.last()

    # Création du contexte
    context = {
        'all_et0': all_et0,
        'all_et0dr': all_et0dr,
        'last_et0': last_et0,
        'last_et0dr': last_et0dr,
        'labels_et0': labels_et0,
        'labels_et0dr': labels_et0dr,
        'data_et0': data_et0,
        'data_et0dr': data_et0dr,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d"),
    }

    return render(request, "enviro/hum15.html", context)
# def wind_rose_data(request):
#     # Filtrer les données sur les 7 derniers jours
#     wind_data = wsd.objects.filter(Time_Stamp__gte=timezone.now() - timezone.timedelta(days=7)).values_list('wind_direction', flat=True)

#     # Compter les occurrences de chaque direction
#     direction_counts = Counter(wind_data)

#     # Calculer le pourcentage
#     total = sum(direction_counts.values())
#     wind_percentages = [{"direction": direction, "percentage": round((count / total) * 100, 2)} for direction, count in direction_counts.items()]

#     return JsonResponse(wind_percentages, safe=False)

# from django.shortcuts import render
# import json

# def mych(request):
#     # Supposons que vous avez des données de ventes et des catégories de l'année
#     sales_data = [30, 40, 35, 50, 49, 60, 70, 91, 125]
#     categories_data = [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]

#     # Convertir les données en JSON
#     sales_data_json = json.dumps(sales_data)
#     categories_data_json = json.dumps(categories_data)

#     # Affichez le contenu de votre contexte pour le débogage
#     print("Sales data JSON:", sales_data_json)
#     print("Categories data JSON:", categories_data_json)

#     # Passer les données vers le modèle HTML
#     context = {
#         'sales_data_json': sales_data_json,
#         'categories_data_json': categories_data_json,
#     }

#     # Rendre le modèle HTML avec les données
#     return render(request, 'test.html', context)

# Configuration de ChirpStack
CHIRPSTACK_API_URL = "http://213.32.91.140:8080/api/devices/ce7554dc00001057/queue"
CHIRPSTACK_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjY5NTMzMjAxLWFmMzYtNDliNS05MjQxLTE5ZTBjMTg4MDFhMiIsInR5cCI6ImtleSJ9.klR4xIax_a1IOf5nDLlhosJHSU7_fmtCio1Jd6MGHJs"  # Remplace avec ta clé API
@csrf_exempt
def send_command(request):
    if request.method == "POST":
        command = request.POST.get("command")  # "ON" ou "OFF"
        value = request.POST.get("value")  # Valeur entière (0-255)

        if not command or not value:
            return render(request, "control.html", {"error": "Commande ou valeur manquante !"})

        # Convertir ON/OFF en binaire
        command_bin = 1 if command == "ON" else 0
        value_int = int(value)

        # Création du payload : [ON/OFF, valeur]
        payload_bytes = bytes([command_bin, value_int])
        payload_hex = payload_bytes.hex()  # Conversion en hexadécimal

        headers = {
            "Content-Type": "application/json",
            "Grpc-Metadata-Authorization": f"Bearer {CHIRPSTACK_API_KEY}"
        }

        payload = {
            "deviceQueueItem": {
                "confirmed": True,
                "fPort": 1,
                "data": payload_hex  # Encodé en hexadécimal
            }
        }

        response = requests.post(CHIRPSTACK_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return render(request, "control.html", {"success": "Commande envoyée avec succès !"})
        else:
            return render(request, "control.html", {"error": f"Échec de l'envoi ! {response.text}"})

    return render(request, "control.html")

from django.utils.timezone import now

def compare_sensors(request):
    # Définir la date limite (3 jours avant aujourd'hui)
    date_limite = now() - pd.Timedelta(days=3)

    # Récupérer les données des capteurs
    ref_data = Ray2.objects.filter(DateRay__gte=date_limite).values("DateRay", "Ray")
    dragino_data = wsd.objects.filter(Time_Stamp__gte=date_limite).values("Time_Stamp", "illumination")

    # Convertir en DataFrame pandas
    ref_df = pd.DataFrame(list(ref_data)).rename(columns={"DateRay": "timestamp", "Ray": "sensecap"})
    dragino_df = pd.DataFrame(list(dragino_data)).rename(columns={"Time_Stamp": "timestamp", "illumination": "dragino"})

    # Vérifier s'il y a assez de données
    if ref_df.empty or dragino_df.empty:
        return JsonResponse({"error": "Pas assez de données sur les 3 derniers jours"}, status=400)

    # Filtrer les valeurs extrêmes (exemple : valeurs supérieures à 2000 W/m² ou nulles)
    ref_df = ref_df[(ref_df["sensecap"] > 0) & (ref_df["sensecap"] < 2000)]
    dragino_df = dragino_df[(dragino_df["dragino"] > 0) & (dragino_df["dragino"] < 2000)]

    # Vérifier si les données sont encore valides après filtrage
    if ref_df.empty or dragino_df.empty:
        return JsonResponse({"error": "Toutes les valeurs valides ont été filtrées"}, status=400)

    # Ajouter une colonne de date uniquement (sans l'heure) pour extraire la valeur maximale par jour
    ref_df["date"] = ref_df["timestamp"].dt.date
    dragino_df["date"] = dragino_df["timestamp"].dt.date

    # Calculer les valeurs maximales par jour
    max_ref = ref_df.groupby("date")["sensecap"].max().reset_index()
    max_dragino = dragino_df.groupby("date")["dragino"].max().reset_index()

    # Fusionner les résultats maximaux des deux capteurs sur la colonne 'date'
    max_df = pd.merge(max_ref, max_dragino, on="date", how="inner")

    # Vérifier si les données maximales existent
    if max_df.empty:
        return JsonResponse({"error": "Pas de données maximales disponibles"}, status=400)

    # Calculer le facteur de calibration pour chaque jour en comparant les valeurs maximales
    max_df["calibration_factor"] = max_df["sensecap"] / max_df["dragino"]

    # Calculer la moyenne du facteur de calibration pour l'ensemble des jours
    avg_calibration_factor = max_df["calibration_factor"].mean()

    # Appliquer l'inverse du facteur de calibration (pour diminuer la valeur de dragino)
    dragino_df["calibrated_dragino"] = dragino_df["dragino"] / avg_calibration_factor

    # Fusionner les données de calibration avec celles de sensecap sur la base de 'date' (et non 'timestamp')
    merged_df = pd.merge(dragino_df, ref_df[["timestamp", "sensecap", "date"]], on="date", how="left")

    # Retourner les résultats en JSON avec les valeurs calibrées et les valeurs de sensecap
    return JsonResponse({
        "calibration_factor": round(avg_calibration_factor, 2),
        "calibrated_values": merged_df[["timestamp", "sensecap", "dragino", "calibrated_dragino"]].to_dict(orient="records")
    })

# if data['deviceInfo']['devEui']==pyranometre:
                #     time_test = datetime.datetime.now()
                #     hour_minute = time_test.strftime('%H:%M')
                #     print("***************************************pyranometre")
                #     print(hour_minute)
                #     payload_data = data["object"]["bytes"]
                #     xpayload_data = [int(_byte) for _byte in payload_data]
                #     taille_xpayload_data = len(xpayload_data)
                #     print(xpayload_data)
                #     print(taille_xpayload_data)
                #     if taille_xpayload_data == 8:
                #         ray = (xpayload_data[0]*256 + xpayload_data[1])
                #         print(ray)
                #         v_batt = (xpayload_data[2] * 256) + xpayload_data[3]
                #         v_batt = float(v_batt/100)
                #         print(v_batt)
                #         db_obj = Ray()
                #         db_obj.Bat = v_batt
                #         db_obj.Ray = ray
                #         db_obj.save()
                #         print("******* les données du pyra sont bien registées")




                # if (data['deviceInfo']['devEui']== black_device_eui or data['deviceInfo']['devEui']==  red_device_eui):
                #     payload_data= data['object']['bytes']
                #     xpayload_data= [int(_byte) for _byte in payload_data]
                #     taille_xpayload_data = len(xpayload_data)
                #     print(xpayload_data)
                #     print(taille_xpayload_data)
                #     if taille_xpayload_data == 14:
                #         temp = (xpayload_data[0] * 256) + xpayload_data[1]
                #         temp = float(temp/100)

                #         hum = (xpayload_data[2] * 256) + xpayload_data[3]
                #         hum = float(hum/100)

                #         ec = (xpayload_data[4] * 256) + xpayload_data[5]
                #         ec = float(ec)

                #         sal = (xpayload_data[6] * 256) + xpayload_data[7]
                #         sal = float(sal)

                #         v_batt = (xpayload_data[8] * 256) + xpayload_data[9]
                #         v_batt = float(v_batt/100)

                #         deepsleep = (xpayload_data[13] << 24)  + (xpayload_data[12] << 16) + (xpayload_data[11] << 8) + (xpayload_data[10])
                #         print('deepsleep : ', deepsleep)
                #         if data['deviceInfo']['devEui']== black_device_eui:
                #             db_obj= CapSol()
                #             db_obj.devId= 2
                #             db_obj.Temp= temp
                #             db_obj.Hum= hum
                #             db_obj.Ec= ec
                #             db_obj.Sal= sal
                #             db_obj.Bat= v_batt
                #             db_obj.save()
                #         else:
                #             db_obj= CapSol2()
                #             db_obj.devId= 3
                #             db_obj.Temp= temp
                #             db_obj.Hum= hum
                #             db_obj.Ec= ec
                #             db_obj.Sal= sal
                #             db_obj.Bat= v_batt
                #             db_obj.save()
                #     else :
                #         print("ya pas des données????!!!!")
                #         v_batt = (xpayload_data[0] * 256) + xpayload_data[1]
                #         v_batt = float(v_batt/100)
                #         print(v_batt)
                #         deepsleep = (xpayload_data[5] << 24)  + (xpayload_data[4] << 16) + (xpayload_data[3] << 8) + (xpayload_data[2])
                #         print('deepsleep : ', deepsleep)

                # if data['deviceInfo']['devEui']==npk_device_eui:
                #     payload_data= data['object']['bytes']
                #     xpayload_data= [int(_byte) for _byte in payload_data]
                #     taille_xpayload_data = len(xpayload_data)
                #     print(xpayload_data)
                #     print(taille_xpayload_data)
                #     if taille_xpayload_data == 12:
                #         azt = xpayload_data[0]*256 + xpayload_data[1]
                #         azt = float(azt)
                #         pho = xpayload_data[2]*256 + xpayload_data[3]
                #         pho = float(pho)
                #         pot = xpayload_data[4]*256 + xpayload_data[5]
                #         pot = float(pot)
                #         v_batt = xpayload_data[6]*256 + xpayload_data[7]
                #         v_batt = float(v_batt/100)
                #         deepsleep = (xpayload_data[8]) + (xpayload_data[9] << 8) + (xpayload_data[10] << 16) + (xpayload_data[11] << 24)
                #         print(azt)
                #         db_obj= CapNPK()
                #         db_obj.devId=4
                #         db_obj.Azoute= azt
                #         db_obj.Phosphore= pho
                #         db_obj.Potassium= pot
                #         db_obj.Bat= v_batt
                #         db_obj.save()
                #         print("deepsleep : ", deepsleep)
                #     else :
                #         print("ya pas des données????!!!!")
                #         v_batt = (xpayload_data[0] * 256) + xpayload_data[1]
                #         v_batt = float(v_batt/100)
                #         print(v_batt)
                #         deepsleep = (xpayload_data[5] << 24)  + (xpayload_data[4] << 16) + (xpayload_data[3] << 8) + (xpayload_data[2])
                #         print('deepsleep : ', deepsleep)

                # object_wsd = wsd()
                    # object_wsd.wind_direction_angle = data['object']['wind_direction_angle']  # Direction du vent en degrés
                    # print(data['object']['wind_direction_angle'])
                    # object_wsd.wind_direction = data['object']['wind_direction']  # Direction du vent ('E' pour Est)
                    # object_wsd.HUM = data['object']['TEM']  # Humidité
                    # object_wsd.rain_gauge = data['object']['rain_gauge']  # Pluviométrie
                    # object_wsd.wind_speed = data['object']['wind_speed']  # Vitesse du vent
                    # object_wsd.illumination = data['object']['illumination']  # Illumination
                    # object_wsd.TEM = data['object']['HUM']  # Température
                    # object_wsd.pressure = data['object']['pressure']  # Pression
                    # D'autres champs peuvent être affectés de manière similaire

                    # Attribution des valeurs aux champs de l'objet à partir du dictionnaire
                    # object_wsd.wind_direction_angle = wind_direction_angle  # Direction du vent en degrés
                    # object_wsd.wind_direction = wind_direction # Direction du vent (ex: 'E' pour Est)
                    # object_wsd.HUM = TEM  # Humidité
                    # object_wsd.rain_gauge = rain_gauge  # Pluviométrie

                    # object_wsd.wind_speed = wind_speed  # Vitesse du vent
                    # object_wsd.illumination = illumination  # Illumination

                    # object_wsd.TEM = HUM  # Température
                    # object_wsd.save()

                    # Vous pouvez aussi imprimer l'objet pour vérifier
                    # print(object_wsd)
                    # object_wsd.PM2_5 = 0.0  # Particules fines PM2.5
                    # object_wsd.PM10 = 0.0  # Particules fines PM10
                    # object_wsd.TSR = 0.0  # Taux de réflectance solaire (ou autre valeur si vous avez une autre signification)
                    # object_wsd.wind_speed_level = 0.0  # Niveau de la vitesse du vent
                    # object_wsd.pressure = 48.8  # Pression
                    # object_wsd.CO2 = 0.0  # CO2
                    # Sauvegarde de l'objet dans la base de données

                #     payload_data= data['object']['bytes']
                #     xpayload_data= [int(_byte) for _byte in payload_data]
                #     taille_xpayload_data = len(xpayload_data)
                #     print(xpayload_data)
                #     print(taille_xpayload_data)
                #     batt = (xpayload_data[0]*256 + xpayload_data[1])/1000
                #     temp1 = (xpayload_data[3]*256 + xpayload_data[4])/10
                #     hum1 = (xpayload_data[5]*256 + xpayload_data[6])/10
                #     ce1 = xpayload_data[7]*256 + xpayload_data[8]
                #     azt1 = xpayload_data[9]*256 + xpayload_data[10]
                #     pho1 = xpayload_data[11]*256 + xpayload_data[12]
                #     pot1 = xpayload_data[13]*256 + xpayload_data[14]

                #     hum2 = (xpayload_data[15]*256 + xpayload_data[16])/10
                #     temp2 = (xpayload_data[17]*256 + xpayload_data[18])/10
                #     ce2 = xpayload_data[19]*256 + xpayload_data[20]
                #     azt2 = xpayload_data[21]*256 + xpayload_data[22]
                #     pho2 = xpayload_data[23]*256 + xpayload_data[24]
                #     pot2 = xpayload_data[25]*256 + xpayload_data[26]

                #     temp3 = (xpayload_data[27]*256 + xpayload_data[28])/100
                #     hum3 = (xpayload_data[29]*256 + xpayload_data[30])/100
                #     ce3 = xpayload_data[31]*256 + xpayload_data[32]
                #     sal3 = xpayload_data[33]*256 + xpayload_data[34]

                #     azt3 = xpayload_data[35]*256 + xpayload_data[36]
                #     pho3 = xpayload_data[37]*256 + xpayload_data[38]
                #     pot3 = xpayload_data[39]*256 + xpayload_data[40]

                #     db_obj_THSCE= CapSol()
                #     db_obj_THSCE.devId = 2
                #     db_obj_THSCE.Temp = temp3
                #     db_obj_THSCE.Hum = hum3
                #     db_obj_THSCE.Sal = sal3
                #     db_obj_THSCE.EC = ce3
                #     db_obj_THSCE.Bat = batt
                #     db_obj_THSCE.save()

                #     db_obj_NPK = CapNPK()
                #     db_obj_NPK.devId = 4
                #     db_obj_NPK.Azoute = azt3
                #     db_obj_NPK.Phosphore = pho3
                #     db_obj_NPK.Potassium = pot3
                #     db_obj_NPK.Bat = batt
                #     db_obj_NPK.save()

                #     db_obj_THSCEAPh1 = CapTHSCEAPhPo1()
                #     db_obj_THSCEAPh1.Temp = temp1
                #     db_obj_THSCEAPh1.Hum = hum1
                #     db_obj_THSCEAPh1.CE = ce1
                #     db_obj_THSCEAPh1.Azoute = azt1
                #     db_obj_THSCEAPh1.Phosphore = pho1
                #     db_obj_THSCEAPh1.Potassium = pot1
                #     db_obj_THSCEAPh1.Bat = batt
                #     db_obj_THSCEAPh1.save()

                #     db_obj_THSCEAPh = CapTHSCEAPhPo()
                #     db_obj_THSCEAPh.Temp = temp2
                #     db_obj_THSCEAPh.Hum = hum2
                #     db_obj_THSCEAPh.CE = ce2
                #     db_obj_THSCEAPh.Azoute = azt2
                #     db_obj_THSCEAPh.Phosphore = pho2
                #     db_obj_THSCEAPh.Potassium = pot2
                #     db_obj_THSCEAPh.Bat = batt
                #     db_obj_THSCEAPh.save()

                # if data['deviceInfo']['devEui'] == 'a84041b02458e028':
                #     messages = data['object']['messages']
                #     print("messages WEATHER STATION : ", messages)

 # {'wind_direction_angle': 201.2, 'wind_direction': 'E', 'HUM': 16.7, 'rain_gauge': 51.2,
    # 'CO2': 0.0, 'wind_speed': 0.0, 'illumination': 0.0, 'wind_speed_level': 0.0, 'pressure': 48.8, 'TEM': 57.2, 'PM2_5': 0.0, 'PM10': 0.0, 'TSR': 0.0}
                    # Attribution des valeurs aux champs de l'objet
                    # Instanciation de l'objet wsd
                    # object_wsd = wsd(
                    #     wind_direction_angle=201.2,
                    #     wind_direction='E',
                    #     HUM=16.7,
                    #     rain_gauge=51.2,
                    #     wind_speed=5.0,
                    #     illumination=10.0,
                    #     TEM=22.5
                    #     # pressure=1013.0
                    # )
                    # object_wsd.save()
                    # object_wsd.pressure = object_data.get('pressure', None)
                    # object_wsd.CO2 = object_data.get('CO2', None)
                    # object_wsd.wind_speed_level = object_data.get('wind_speed_level', None)
                    # object_wsd.TSR = object_data.get('TSR', None)
                    # object_wsd.PM2_5 = object_data.get('PM2_5', None)
                    # object_wsd.PM10 = object_data.get('PM10', None)