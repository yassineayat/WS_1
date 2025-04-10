import datetime
import math
import os
import sys
import penmon as pm

import django
from django.conf import settings
from django.db.models import Sum, Avg, Max, Min
from django.utils import timezone

project_home = '/home/wsensa/ws_irr'  # Replace with the actual path to your project
if project_home not in sys.path:
    sys.path.append(project_home)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prjt.settings')  # Replace 'prjt.settings' with your actual settings module

django.setup()
from application.models import Ray2, Data2, ET0o, DataFwiO

def FWI():
    class FWICLASS:
        def __init__(self, temp, rhum, wind, prcp):
            self.h = rhum
            self.t = temp
            self.w = wind
            self.p = prcp

        def FFMCcalc(self, ffmc0):
            mo = (147.2 * (101.0 - ffmc0)) / (59.5 + ffmc0)
            if self.p > 0.5:
                rf = self.p - 0.5
                if mo > 150.0:
                    mo = (mo + 42.5 * rf * math.exp(-100.0 / (251.0 - mo)) * (1.0 - math.exp(-6.93 / rf))) + (0.0015 * (mo - 150.0) ** 2) * math.sqrt(rf)
                else:
                    mo = mo + 42.5 * rf * math.exp(-100.0 / (251.0 - mo)) * (1.0 - math.exp(-6.93 / rf))
                if mo > 250.0:
                    mo = 250.0
            ed = .942 * (self.h ** .679) + (11.0 * math.exp((self.h - 100.0) / 10.0)) + 0.18 * (21.1 - self.t) * (1.0 - 1.0 / math.exp(.1150 * self.h))
            if mo < ed:
                ew = .618 * (self.h ** .753) + (10.0 * math.exp((self.h - 100.0) / 10.0)) + .18 * (21.1 - self.t) * (1.0 - 1.0 / math.exp(.115 * self.h))
                if mo <= ew:
                    kl = .424 * (1.0 - ((100.0 - self.h) / 100.0) ** 1.7) + (.0694 * math.sqrt(self.w)) * (1.0 - ((100.0 - self.h) / 100.0) ** 8)
                    kw = kl * (.581 * math.exp(.0365 * self.t))
                    m = ew - (ew - mo) / 10.0 ** kw
                else:
                    m = mo
            elif mo == ed:
                m = mo
            else:
                kl = .424 * (1.0 - (self.h / 100.0) ** 1.7) + (.0694 * math.sqrt(self.w)) * (1.0 - (self.h / 100.0) ** 8)
                kw = kl * (.581 * math.exp(.0365 * self.t))
                m = ed + (mo - ed) / 10.0 ** kw
            ffmc = (59.5 * (250.0 - m)) / (147.2 + m)
            if ffmc > 101.0:
                ffmc = 101.0
            if ffmc <= 0.0:
                ffmc = 0.0
            return ffmc

        def DMCcalc(self, dmc0, mth):
            el = [6.5, 7.5, 9.0, 12.8, 13.9, 13.9, 12.4, 10.9, 9.4, 8.0, 7.0, 6.0]
            t = self.t
            if t < -1.1:
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
                    else:
                        b = 6.2 * math.log(dmc0) - 17.2
                wmr = wmi + (1000 * rw) / (48.77 + b * rw)
                pr = 43.43 * (5.6348 - math.log(wmr - 20.0))
            else:
                pr = dmc0
            if pr < 0.0:
                pr = 0.0
            dmc = pr + rk
            if dmc <= 1.0:
                dmc = 1.0
            return dmc

        def DCcalc(self, dc0, mth):
            fl = [-1.6, -1.6, -1.6, 0.9, 3.8, 5.8, 6.4, 5.0, 2.4, 0.4, -1.6, -1.6]
            t = self.t
            if t < -2.8:
                t = -2.8
            pe = (0.36 * (t + 2.8) + fl[mth - 1]) / 2
            if pe <= 0.0:
                pe = 0.0
            if self.p > 2.8:
                ra = self.p
                rw = 0.83 * ra - 1.27
                smi = 800.0 * math.exp(-dc0 / 400.0)
                dr = dc0 - 400.0 * math.log(1.0 + ((3.937 * rw) / smi))
                if dr > 0.0:
                    dc = dr + pe
            else:
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
            if bb <= 1.0:
                fwi = bb
            else:
                fwi = math.exp(2.72 * (0.434 * math.log(bb)) ** 0.647)
            return fwi

    def main():
        one_day_ago = (timezone.now() - datetime.timedelta(days=1)).replace(hour=13, minute=30, second=0, microsecond=0)
        now = timezone.now().replace(hour=13, minute=30, second=0, microsecond=0)
        posts = Data2.objects.filter(Time_Stamp__range=(one_day_ago, now))
        totalVent = posts.aggregate(Sum('Wind_Speed'))['Wind_Speed__sum'] or 0
        nbrVent = posts.count()
        wind = round((totalVent / nbrVent), 2) if nbrVent else 0

        Maxtemp = posts.aggregate(Max('Temp'))['Temp__max'] or 0
        Mintemp = posts.aggregate(Min('Temp'))['Temp__min'] or 0
        temp = (Maxtemp + Mintemp) / 2

        MaxHum = posts.aggregate(Max('Hum'))['Hum__max'] or 0
        MinHum = posts.aggregate(Min('Hum'))['Hum__min'] or 0
        rhum = (MaxHum + MinHum) / 2
        if rhum > 100.0:
            rhum = 100.0

        totalrain = posts.aggregate(Sum('Rain'))['Rain__sum'] or 0
        nmbrRain = posts.count()
        prcp = totalrain / nmbrRain if nmbrRain else 0

        initfw = DataFwiO.objects.last()
        ffmc0 = initfw.ffmc if initfw else 85
        dmc0 = initfw.dmc if initfw else 6
        dc0 = initfw.dc if initfw else 15

        mth = datetime.datetime.today().month
        fwisystem = FWICLASS(temp, rhum, wind, prcp)
        ffmc = fwisystem.FFMCcalc(ffmc0)
        dmc = fwisystem.DMCcalc(dmc0, mth)
        dc = fwisystem.DCcalc(dc0, mth)
        isi = fwisystem.ISIcalc(ffmc)
        bui = fwisystem.BUIcalc(dmc, dc)
        fwi = fwisystem.FWIcalc(isi, bui)

        date_time = timezone.now()
        ffmc_round = round(ffmc, 1)
        dmc_round = round(dmc, 1)
        dc_round = round(dc, 1)
        isi_round = round(isi, 1)
        bui_round = round(bui, 1)
        fwi_round = round(fwi, 2)

        print(f"ffmc: {ffmc_round}, dmc: {dmc_round}, dc: {dc_round}, isi: {isi_round}, bui: {bui_round}, fwi: {fwi_round}, date_time: {date_time}")

        try:
            # Initial query without Time_Stamp filter
            existing_objs = DataFwiO.objects.filter(
                ffmc=ffmc_round, dmc=dmc_round, dc=dc_round, isi=isi_round,
                bui=bui_round, fwi=fwi_round
            )
            print(f"Existing objects without date filter: {existing_objs}")

            if not existing_objs.exists():
                DataFwiO.objects.create(
                    ffmc=ffmc_round, dmc=dmc_round, dc=dc_round, isi=isi_round,
                    bui=bui_round, fwi=fwi_round
                )
                print("ok")
            print("__________________________________FWI Calculé________________________________")
        except Exception as e:
            print(f"Error during query: {e}")

    main()

FWI()
def ET0o_calc():
    one_day_ago = (timezone.now() - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    radiation_data = Ray2.objects.filter(DateRay__range=(one_day_ago, now)).aggregate(Avg('Ray'))
    print(radiation_data)
    radiation_avg = radiation_data['Ray__avg']

    weather_data = Data2.objects.filter(Time_Stamp__range=(one_day_ago, now)).aggregate(
        Avg('Temp'),
        Avg('Hum'),
        Avg('Wind_Speed'),
        Avg('Pr')
    )
    temp_avg = weather_data['Temp__avg']
    hum_avg = weather_data['Hum__avg']
    wind_speed_avg = round((weather_data['Wind_Speed__avg'] / 3.6), 4)
    pressure_avg = weather_data['Pr__avg']

    station = pm.Station(latitude=33.51, altitude=532)
    station.anemometer_height = 2
    print("radiation :",radiation_avg)
    r1 = round((radiation_avg * 0.0864), 2)
    print("r1 :",r1)
    temp_max = Data2.objects.filter(Time_Stamp__range=(one_day_ago, now)).order_by('-Temp').first().Temp
    temp_min = Data2.objects.filter(Time_Stamp__range=(one_day_ago, now)).order_by('Temp').first().Temp
    humidity_max = Data2.objects.filter(Time_Stamp__range=(one_day_ago, now)).order_by('-Hum').first().Hum
    humidity_min = Data2.objects.filter(Time_Stamp__range=(one_day_ago, now)).order_by('Hum').first().Hum
    day_of_year = (timezone.now().timetuple().tm_yday - 1)
    print("day_of_year :", day_of_year)
    day = station.day_entry(
        day_of_year,
        temp_max=temp_max,
        temp_min=temp_min,
        # temp_mean=temp_avg,
        wind_speed=wind_speed_avg,
        humidity_max=humidity_max,
        humidity_min=humidity_min,
        radiation_s=r1
    )

    eto_value = round((day.eto()), 2)
    print("ETo for this day is", eto_value)

    ET0o.objects.create(value=eto_value, WSavg=wind_speed_avg, Tmax=temp_max, Tmin=temp_min, Hmax=humidity_max, Hmin=humidity_min, Raym=round(radiation_avg,2), U2=wind_speed_avg, Delta=day_of_year)

ET0o_calc()