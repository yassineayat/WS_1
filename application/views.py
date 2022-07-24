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
                return HttpResponseRedirect('/Chart')

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
    lstet = ET0.objects.last()
    lstfwi= DataFwi.objects.last()
    # exemple() FWI
    one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    posts = Ws.objects.filter(date__gte=one_day_ago)
    print("posts :", posts)
    #vent calcul
    totalVent = posts.values('Vent').aggregate(Sum('Vent'))
    nbrVent = posts.values('Vent').count()
    moyVent=round((totalVent["Vent__sum"]/nbrVent),2)
    print("totalevent : ",totalVent , nbrVent, moyVent)
    #temperature calcul
    Maxtemp = posts.values('Temperature').aggregate(Max('Temperature'))
    Mintemp = posts.values('Temperature').aggregate(Min('Temperature'))
    moyTemp = (Maxtemp["Temperature__max"] + Mintemp["Temperature__min"]) / 2
    print("moyTemp :", moyTemp)
    #humiidity calcul
    MaxHum = posts.values('Humidity').aggregate(Max('Humidity'))
    MinHum = posts.values('Humidity').aggregate(Min('Humidity'))
    moyHum = (MaxHum["Humidity__max"] + MinHum["Humidity__min"]) / 2
    print("moyHum : ", moyHum)
    #pluie calcul
    totalrain = posts.values('Pluv').aggregate(Sum('Pluv'))
    nmbrRain = posts.values('Pluv').count()
    moyRain = totalrain['Pluv__sum']/nmbrRain
    print("moyRain :", moyRain)
    mth = datetime.datetime.today().month
    print(mth)


    context={'lst':lst,'t':t,'h':h,'v':v,'r':r,'p':p,"lstet":lstet,'lstfwi':lstfwi}
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