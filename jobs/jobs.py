import datetime
import math
import time

from django.conf import settings
import requests
import json
import random

from django.db.models import Sum, Avg, Max, Min

from application.models import Ws, ET0, DataFwi,Ray

postcodes = [
    "SW1A 1AA",
    "PE35 6EB",
    "CV34 6AH",
    "EH1 2NG"
]


def schedule_api():

    postcode = postcodes[random.randint(0, 3)]

    full_url = f"https://api.postcodes.io/postcodes/{postcode}"

    r = requests.get(full_url)
    if r.status_code == 200:
        result = r.json()["result"]

        lat = result["latitude"]
        lng = result["longitude"]

        print(f'Latitude: {lat}, Longitude: {lng}')
        print(datetime.datetime.now()-datetime.timedelta(1))


def schedule_api2():
    headers = {
        'authorization': '876523763964578',
    }
    params = (
        ('type', 'value'),
    )
    response = requests.get('https://api.myiotplatform.com/data/exports/devices/d1072befe4', headers=headers,
                            params=params)
    response2 = requests.get('https://api.myiotplatform.com/data/exports/devices/f29f3c49e0', headers=headers,
                            params=params)
    pouet = json.loads(response.text)
    pouet2 = json.loads(response2.text)
    i=-1
    dateobservation = str(pouet['data']['d1072befe4'][i]['dateEvent'])
    dateobservation2 = str(pouet2['data']['f29f3c49e0'][i]['dateEvent'])
    if not Ws.objects.filter(date=dateobservation).exists():
        # dobservation_str = dateobservation[0:10]
        # heureobservation = dateobservation[11:19]
        # print("dobservation_str :" + dobservation_str)
        # print("heureobservation :" + heureobservation)

        # print("test" + str(pouet['data']['d1072befe4'][i]['data']['probe1']['value']))
        temperature = pouet['data']['d1072befe4'][i]['data']['probe1']['value']

        hygro = pouet['data']['d1072befe4'][i]['data']['probe2']['value']

        vitvent = pouet['data']['d1072befe4'][i]['data']['probe3']['value']

        rafale = pouet['data']['d1072befe4'][i]['data']['probe4']['value']
        pluvio = pouet['data']['d1072befe4'][i]['data']['probe5']['value']

        Ray = pouet2['data']['f29f3c49e0'][i]['data']['probe1']['value']

        # if not Ws.objects.filter(date=dateobservation).exists():
            # Insert new data here
        tab = Ws.objects.create(Temperature=temperature, Humidity=hygro, Vent=vitvent, Rafale=rafale, Pluv=pluvio,Ray=Ray,
                                date=dateobservation, dateRay=dateobservation2)
        print(tab)
        print(datetime.datetime.now()-datetime.timedelta(1))
    # time.sleep(1)

    else:
        print("deja existe")

def schedule_api3():
    headers = {
        'authorization': '876523763964578',
    }
    params = (
        ('type', 'value'),
    )

    response2 = requests.get('https://api.myiotplatform.com/data/exports/devices/f29f3c49e0', headers=headers,
                            params=params)

    pouet2 = json.loads(response2.text)
    i=-1
    dateobservation2 = str(pouet2['data']['f29f3c49e0'][i]['dateEvent'])
    print(dateobservation2)
    if not Ray.objects.filter(dateRay=dateobservation2).exists():
        Rayo = pouet2['data']['f29f3c49e0'][i]['data']['probe1']['value']

        # if not Ws.objects.filter(date=dateobservation).exists():
            # Insert new data here
        tab = Ray.objects.create(Ray=Rayo, dateRay=dateobservation2)
        print(tab)
        print(datetime.datetime.now()-datetime.timedelta(1))
    # time.sleep(1)

    else:
        print("deja existe rayonnement")

def ET0_calc():

    one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    print(one_day_ago.strftime("%d"))
    # day = datetime.datetime.now().strftime("%d")
    # print("day",day)
    lstet = ET0.objects.last()
    # exemple()
    day = datetime.datetime.today().date()
    print("day", day)
    x = ET0.objects.last()
    print("eto", (x.dt))
    # if ET0.objects.filter(dt=x.dt).exists():
    #     print("Ok")
    # else:
    posts = Ws.objects.filter(date__gte=one_day_ago)
    posts2 = Ray.objects.filter(dateRay__gte=one_day_ago)
    print("posts", posts)
    totalRay = posts2.values('Ray').aggregate(Sum('Ray'))
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
    print("avgWS :", avgvent)
    B2 = one_day_ago.timetuple().tm_yday
    RS = Rayt  # totl radiation
    Tmin = Tmmin
    Tmax = Tmmax
    HRmin = Hmin
    HRmax = Hmax
    u = avgvent  # m/s moyen
    M = RS / 24  # radiation/h
    N = M * 3600 * 0.000001 * 24  # Rs [MJm-2d-1]
    u2 = u * 4.87 / math.log(67.8 * 2 - 5.42)
    latitude = 33.51
    altitude = 755
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
    ET = (0.408 * AJ * (AH - AI) + (1600 * g / ((Tmin + Tmax) * 0.5 + 273)) * u2 * (AE - AF)) / (
            AJ + g * (1 + 0.38 * u2))
    ET_0 = round(ET, 2)
    print("ET_0", ET_0)

    ET0.objects.create(value=ET_0, WSavg=avgvent, Tmax=Tmax, Tmin=Tmin, Hmax=HRmax, Hmin=HRmin, Raym=Rayt, U2=u2, Delta=B2)
    print("__________________________________ET_O Calculé________________________________")

def FWI():
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
        print("moyTemp :", temp)
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
        print("ffmc0 :", ffmc0)
        dmc0 = initfw.dmc
        print("dmc0 :", dmc0)
        dc0 = initfw.dc
        print("dc0 :", dc0)
        mth = datetime.datetime.today().month
        print(mth)  # 4
        fwisystem = FWICLASS(temp, rhum, wind, prcp)
        ffmc = fwisystem.FFMCcalc(ffmc0)
        dmc = fwisystem.DMCcalc(dmc0, mth)
        dc = fwisystem.DCcalc(dc0, mth)
        isi = fwisystem.ISIcalc(ffmc)
        bui = fwisystem.BUIcalc(dmc, dc)
        fwi = fwisystem.FWIcalc(isi, bui)
        DataFwi.objects.create(ffmc=round(ffmc, 1), dmc=round(dmc, 1), dc=round(dc, 1), isi=round(isi, 1),
                               bui=round(bui, 1), fwi=round(fwi, 2))
        print("__________________________________FWI Calculé________________________________")

    main()