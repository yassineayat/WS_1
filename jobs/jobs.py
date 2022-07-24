import datetime
import math
import time

from django.conf import settings
import requests
import json
import random

from django.db.models import Sum, Avg, Max, Min

from application.models import Ws, ET0

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
    if ET0.objects.filter(dt=x.dt).exists():
        print("Ok")
    else:
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
        print("ok bien")
