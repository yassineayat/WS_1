# Create your views here.
import datetime
import math

from django.db.models import Max, Min, Sum, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView
import paho.mqtt.client as mqtt

from .models import *
import requests
import json
import penmon as pm




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

""" salinite """
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ray)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "ray/ray1.html", context)

def ray3(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ray)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "ray/ray3.html", context)

def ray7(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Ray)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "ray/ray7.html", context)

def ray15(request):
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=15)).replace(hour=0,minute=0,second=0,microsecond=0)
    labels = []
    dataa = []
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
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
    all = Data.objects.filter(Time_Stamp__gte=one_day_ago)
    # print("all", all)
    for i in all:
        labels.append((i.Time_Stamp).strftime("%Y-%m-%d %H:%M:%S"))
        # print("labels", labels)
        dataa.append(i.Bat)
    lst = Data.objects.last()
    context = {'all': all, 'lst': lst, 'labels': labels, 'dataa': dataa}
    return render(request, "bat/bat15.html", context)
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

def chartec(request):
    tab=CapSol.objects.all()
    labels = []
    dataa = []
    for data in tab:
        labels.append((data.dt).strftime("%Y-%m-%d %H:%M:%S"))
        dataa.append(data.Ec)
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
                dataa.append(data.Ec)

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
                dataa.append(data.Ec)

                print("lab", labels)
                return HttpResponseRedirect('/Chartec')

            print("todate", type(todate))

    context={'tab':tab,'labels':labels,'dataa':dataa}
    return render(request,"chartsec.html",context)

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

    post = Ray.objects.filter(dateRay__gte=one_day_ago, dateRay__lte=now)
    rav = post.count()
    print("nbrs ray1", rav)
    print("____________________________________filtre par heure _______________________________________")

    filtresup=Ray.objects.filter(dateRay__gte=onedayRay,dateRay__lte=todayRay)
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

    cap2 = CapSol2.objects.last()

    bv= batvanne.objects.last()
    # print("last",str((tab.time)))

    f = CapSol.objects.first()
    tab2=CapSol.objects.all()

    max_temp=CapSol.objects.all().aggregate(Max('Temp'))
    min_temp = CapSol.objects.all().aggregate(Min('Temp'))
    moy=(max_temp["Temp__max"]+min_temp["Temp__min"])/2
    print((max_temp["Temp__max"]+min_temp["Temp__min"])/2)

    context = {'tab': tab,'tab2':tab2,'max_temp':max_temp,'min_temp':min_temp,'moy':moy,'f':f}

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

    context = {'tab': tab,'tab2':tab2,'max_temp':max_temp,'min_temp':min_temp,'moy':moy,'f':f,'labels':labels,'dataa':dataa,'dataa2':dataa2,'cap2':cap2, 'bv':bv}
    return render(request, "index.html", context)


    # completed = request.POST('checks')
    # print(completed)
    # if 'checks' in request.GET:

    # toSave = vanne.objects.all()
    # geek_object = vanne.objects.create(onoff=True)
    # geek_object.save()
    # toSave.save()
    # print(toSave)

def wsopen(request):

    now=(datetime.datetime.now()).replace(hour=0,minute=0,second=0,microsecond=0)
    print(now)
    hm = Data.objects.filter(Time_Stamp__gte=now)
    lstfwi = DataFwiO.objects.last()
    """ temperature """
    maxt = hm.aggregate(Max('Temp'))
    dicttolisTmax = list(maxt.items())
    Tmmax = dicttolisTmax[0][1]
    print(Tmmax)
    Tmin = hm.aggregate(Min('Temp'))
    dicttolisTmin = list(Tmin.items())
    Tmmin= dicttolisTmin[0][1]
    print(Tmmin)
    """ humidité """
    Hmmax = hm.aggregate(Max('Hum'))
    Hmmin = hm.aggregate(Min('Hum'))
    dicttolisHmax = list(Hmmax.items())
    dicttolisHmin = list(Hmmin.items())
    Hx= dicttolisHmax[0][1]
    Hm = dicttolisHmin[0][1]

    """ vitesse de vent """
    Wind_Speed_max = hm.aggregate(Max('Wind_Speed'))
    Wind_Speed_min = hm.aggregate(Min('Wind_Speed'))
    dicttolissmax = list(Wind_Speed_max.items())
    dicttolissmin = list(Wind_Speed_min.items())
    Sx = dicttolissmax[0][1]
    Sm = dicttolissmin[0][1]

    """ Rayonnement """
    Ray_max = hm.aggregate(Max('Ray'))
    Ray_min = hm.aggregate(Min('Ray'))
    dicttolisrmax = list(Ray_max.items())
    dicttolisrmin = list(Ray_min.items())
    Rx = dicttolisrmax[0][1]
    Rm = dicttolisrmin[0][1]

    """ Pluie """
    one_hour = (datetime.datetime.now() - datetime.timedelta(hours=1))
    huit_hour = (datetime.datetime.now() - datetime.timedelta(hours=8))
    one_day = (datetime.datetime.now() - datetime.timedelta(days=1))
    print(one_day)
    week=(datetime.datetime.now() - datetime.timedelta(days=7))
    now = datetime.datetime.now()
    y=datetime.datetime.now()-datetime.timedelta(minutes=7)
    x=y.time().strftime("%H:%M:%S")
    posts = Data.objects.filter(Time_Stamp__gte=one_hour,Time_Stamp__lte=now)
    post8 = Data.objects.filter(Time_Stamp__gte=huit_hour,Time_Stamp__lte=now)
    post24 = Data.objects.filter(Time_Stamp__gte=one_day,Time_Stamp__lte=now)
    postweek = Data.objects.filter(Time_Stamp__gte=week,Time_Stamp__lte=now)

    #post24c = Data.objects.filter(Time_Stamp__date=now.date())
    #print(post24c)

    rain1h = posts.aggregate(Avg('Rain'))
    rain8h = post8.aggregate(Avg('Rain'))
    rain24h = post24.aggregate(Avg('Rain'))
    rain7d = postweek.aggregate(Avg('Rain'))
    r1h = list(rain1h.items())
    r8h = list(rain8h.items())
    r24h = list(rain24h.items())
    rw = list(rain7d.items())
    if r1h[0][1] is not None:
        p1h = round(r1h[0][1], 2)
    else:
        p1h = 0  # Set a default value if r1h[0][1] is None
    # p1h = round(r1h[0][1],3)
    if r8h[0][1] is not None:
        p8h = round(r8h[0][1], 2)
    else:
        p8h = 0  # Set a default value if r1h[0][1] is None
    # p8h = round(r8h[0][1],2)
    if r24h[0][1] is not None:
        p24h = round(r24h[0][1], 2)
    else:
        p24h = 0  # Set a default value if r1h[0][1] is None
    # p24h = round(r24h[0][1],2)

    if rw[0][1] is not None:
        p1w = round(rw[0][1], 2)
    else:
        p1w = 0  # Set a default value if r1h[0][1] is None
    # client = mqtt.Client()
    #
    # client.connect("broker.hivemq.com", 1883, 80)
    # # client.reinitialise()
    # client.publish("et", 35)  # publish the message typed by the user

    # client.disconnect();  # disconnect from server
    # print("ok.......data")

    tab = Data.objects.last()
    eto = ET0o.objects.last()
    # print(eto.value)
    # ET0o_calc()
    # print("-----------------------------//------------------------------")
    # exemple()
    # print("eto", eto)
    context={'tab':tab,'eto':eto,'p1w':p1w, 'p24h':p24h,'p8h':p8h,'p1h':p1h, 'Rx':Rx, 'Rm':Rm, 'Sx':Sx,'Sm':Sm, 'Hx':Hx,
             'Hm':Hm,'Tmmax':Tmmax,'Tmmin':Tmmin,"lstfwi":lstfwi}
    return render(request,"ws_open.html",context)


# def dash(request):
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
#     return render(request,"acc.html",context)


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