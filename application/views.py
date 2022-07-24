# Create your views here.
import datetime
import math

from django.db.models import Max, Min, Sum, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView

from .models import *
import requests
import json



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
            print("created_documents6", created_documents6)

            for data in created_documents6:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Temp)
                dataa2.append(data.Hum)
                print("lab", labels)
                return HttpResponseRedirect('/Chart')

            print("todate", type(todate))

    context={'tab':tab,'labels':labels,'dataa':dataa}
    return render(request,"charts.html",context)


def exemple():
    one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    posts = Ws.objects.filter(dateRay__gte=one_day_ago)
    print("posts", posts)
    totalRay = posts.values('Ray').aggregate(Sum('Ray'))
    totalVent = posts.values('Vent').aggregate(Sum('Vent'))
    Maxtemp = posts.values('Temperature').aggregate(Max('Temperature'))
    Mintemp = posts.values('Temperature').aggregate(Min('Temperature'))
    MaxHum = posts.values('Humidity').aggregate(Max('Humidity'))
    MinHum = posts.values('Humidity').aggregate(Min('Humidity'))
    avreage = posts.aggregate(Avg('Vent'))
    dicttolistRay = list(totalRay.items())
    dicttolistVent = list(avreage.items())
    avgvent = (round(dicttolistVent[0][1] / 3.6, 4))
    Rayt = dicttolistRay[0][1]
    dicttolisTmax = list(Maxtemp.items())
    Tmmax = dicttolisTmax[0][1]
    dicttolisTmin = list(Mintemp.items())
    Tmmin = dicttolisTmin[0][1]
    dicttolisHmax = list(MaxHum.items())
    Hmax = dicttolisHmax[0][1]
    dicttolisHmin = list(MinHum.items())
    Hmin = dicttolisHmin[0][1]
    print("posts", posts)
    print("tv", totalVent)
    print("tr", Rayt)
    print("tmin", Tmmin)
    print("tmax", Tmmax)
    print("hmin", Hmin)
    print("hmax", Hmax)
    print("avg :", avgvent)
    B2 = datetime.datetime.now().timetuple().tm_yday
    RS = Rayt  # totl radiation
    Tmin = Tmmin
    Tmax = Tmmax
    HRmin = Hmin
    HRmax = Hmax
    u = avgvent  # m/s moyen
    M = RS/24  # radiation/h
    N = M * 3600 * 0.000001 * 24  # Rs [MJm-2d-1]
    u2 = u * 4.87 / math.log(67.8 * 2 - 5.42)
    latitude = 33.53
    altitude = 531
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

    print("ET_0",round(ET_0, 2))

def weatherS(request):
    lst=Ws.objects.last()
    t = round(lst.Temperature,1)
    h = round(lst.Humidity)
    v = round(lst.Vent,1)
    r = round(lst.Rafale,1)
    p = round(lst.Pluv,1)
    lstet = ET0.objects.last()
    # exemple()
    day = datetime.datetime.today().date()
    print("day", day)
    x = ET0.objects.last()
    print("eto", (x.dt))
    if ET0.objects.filter(dt=x.dt).exists():
        print("Ok")

    else :
        print("no")
    context={'lst':lst,'t':t,'h':h,'v':v,'r':r,'p':p,"lstet":lstet}
    return render(request,"stationvisio.html",context)


def home(request):
    print("date",str((datetime.datetime.now())))
    print("date2", str((datetime.datetime.now()).strftime("%M")))
    tab=CapSol.objects.last()
    print("last",str((tab.time)))


    f = CapSol.objects.first()
    tab2=CapSol.objects.all()

    max_temp=CapSol.objects.all().aggregate(Max('Temp'))
    min_temp = CapSol.objects.all().aggregate(Min('Temp'))
    moy=(max_temp["Temp__max"]+min_temp["Temp__min"])/2
    print((max_temp["Temp__max"]+min_temp["Temp__min"])/2)

    context = {'tab': tab,'tab2':tab2,'max_temp':max_temp,'min_temp':min_temp,'moy':moy,'f':f}

    #tab2 = CapSol.objects.last().filter(devId='03')
    if (request.method == "POST"):
        if (request.POST.get('btn1', False)):
            new_value_button = vanne(onoff=request.POST.get(
                'btn1'))
            print(request.POST.get('btn1', False))
            new_value_button.save()
            return HttpResponseRedirect('/')

    if (request.method == "POST"):
        if (request.POST.get('btn', False)):
            new_value_button1 = vanne(onoff=request.POST.get(
                'btn'))
            print(request.POST.get('btn', False))
            new_value_button1.save()
            return HttpResponseRedirect('/')

    # if (request.method == "POST"):
    #     fromdate=request.POST.get('startdate')
    #     todate = request.POST.get('enddate')
    #     search=CapSol.objects.raw('select devId,Temp,Hum,Ec,Sal,Bat,dt from CapSol where dt between"'+fromdate+'"and "'+todate+'"')
    #     print(search)
    #     # return HttpResponseRedirect('/')
    #     return render(request, "index.html", {"search":search})
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    date_from2 = datetime.datetime.now() - datetime.timedelta(days=7)
    date_from3 = datetime.datetime.now() - datetime.timedelta(days=14)
    date_from4 = datetime.datetime.now() - datetime.timedelta(days=30)
    created_documents = CapSol.objects.filter(dt__gte=date_from)

    created_documents2 = CapSol.objects.filter(dt__gte=date_from2).count()
    created_documents3 = CapSol.objects.filter(dt__gte=date_from3).count()
    created_documents4 = CapSol.objects.filter(dt__gte=date_from4).count()
    print("created_documents",str(created_documents))
    print("created_documents", str(created_documents2))
    print("created_documents", str(created_documents3))
    print("created_documents", str(created_documents4))
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
        print("labels0",labels)

    print("labelall",labels)
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
            # fromdate = datetime.datetime("07-07")
            created_documents5 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('dt')
            print("created_documents5",created_documents5)
            for data in created_documents5:
                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Temp)
                dataa2.append(data.Hum)
                print("labelfiltter", labels)
                # return HttpResponseRedirect('/')
            # print("labelfiltter",labels)
        if fromdate =="":
            fromdate= first.dt

        if todate == "":
            to = (lastdate.dt)+ datetime.timedelta(days=1)
            todate = to + datetime.timedelta(days=1)
            labels.clear()
            dataa.clear()
            dataa2.clear()
            created_documents6 = CapSol.objects.filter(dt__range=[fromdate, todate]).order_by('id')
            print("created_documents6",created_documents6)

            for data in created_documents6:

                labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
                dataa.append(data.Temp)
                dataa2.append(data.Hum)
                print("lab",labels)
            print("todate", type(todate))



                # print("data", str(dataa))
            # print("created_documents5", str(dataa))
    # else:
    #     return HttpResponseRedirect('/')
    # else :
    #     if (request.method == "POST"):
    #         if (request.POST.get('all', True)):
    #             print(request.POST.get('all', True))
    #             tab3 = CapSol.objects.all()
    #             print("tab3", tab3)
    #             for data in tab3:
    #                 labels.append((data.dt).strftime("%d %b %Y %H:%M:%S"))
    #                 dataa.append(data.Temp)
    #                 dataa2.append(data.Hum)
    #                 # print("label3", labels)
    #                 # return HttpResponseRedirect('/')
    context = {'tab': tab,'tab2':tab2,'max_temp':max_temp,'min_temp':min_temp,'moy':moy,'f':f,'labels':labels,'dataa':dataa,'dataa2':dataa2}
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
    tab = Data.objects.last()
    context={'tab':tab}
    return render(request,"ws_open.html",context)