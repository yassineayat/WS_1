import datetime
import json

from django.utils import timezone

import paho.mqtt.client as mqtt
import django
django.setup()


from application.models import *
# from application.models import vanne

import penmon as pm

### create a station class with known location and elevation
from penmon import DayEntry
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code " + str(rc)) #notify about established connection
    client.message_retry_set(2)
    client.subscribe("mgo", 2)
    client.subscribe("cap2",2)
    client.subscribe("batvanne",2)
    client.subscribe("evapo",2)
    client.subscribe("msg", 2)
    client.subscribe("wa",2)





def on_message(client, userdata, msg):
    ms = msg.payload
    data = str(ms[0: len(ms)])[2:-1]
    # data = str(ms)
    print("Your message:" + data + "' with QoS " + str(msg.qos)) #display received message
    ss = data.split(' ')
    print(ss)

    # da= data.split(',')
    # id = int(ss[0])

    if ss[0]=="44":
        ffmc = ss[1]
        dmc = ss[2]
        dc = ss[3]
        isi = ss[4]
        bui = ss[5]
        fwi = ss[6]
        i=ss[7]
        try:
            if not DataFwiO.objects.filter(i=i).exists():
                DataFwiO.objects.create(ffmc=ffmc, dmc=dmc, dc=dc, isi=isi, bui=bui, fwi=fwi, i=i)
            else:
                print(f"A record with i={i} already exists in the database. Skipping insertion.")
            existing_records = DataFwiO.objects.filter(i=i)
            if existing_records.exists():
                if existing_records.count() > 1:
                    # if there are more than one record with the same value of "i", delete all but the last one
                    existing_records[:-1].delete()
                    print(f"Removed {existing_records.count() - 1} duplicate records with i={i} from the database.")
                else:
                    # if there's only one record with the same value of "i", skip the insertion and print a message
                    print(f"A record with i={i} already exists in the database. Skipping insertion.")
                    return
            print("__________________________________FWI Calculé________________________________")
        except:
            pass
    if ss[0]=="33":
        B2 = int(ss[1])
        temp_max = float(ss[2])
        temp_min = float(ss[3])
        humidity_max = float(ss[4])
        humidity_min = float(ss[5])
        ws = float(ss[6])
        rad = float(ss[7])
        eto = float(ss[8])
        i = int(ss[9])
        print(rad)
        station = pm.Station(latitude=34.41, altitude=567)
        station.anemometer_height = 2
        r = round(rad * 0.0864, 2)
        print(r)
        try:
            if not ET0o.objects.filter(i=i).exists():
                ET0o.objects.create(value=eto, WSavg=ws, Tmax=temp_max, Tmin=temp_min, Hmax=humidity_max, Hmin=humidity_min,
                                    Raym=round(rad, 2), U2=ws, Delta=B2, i=i)
                print("__________________________________ET_O open Calculé________________________________")
            else:
                print(f"A record with i={i} already exists in the database. Skipping insertion.")
            existing_records = ET0o.objects.filter(i=i)
            if existing_records.exists():
                if existing_records.count() > 1:
                    # if there are more than one record with the same value of "i", delete all but the last one
                    existing_records[:-1].delete()
                    print(f"Removed {existing_records.count() - 1} duplicate records with i={i} from the database.")
                else:
                    # if there's only one record with the same value of "i", skip the insertion and print a message
                    print(f"A record with i={i} already exists in the database. Skipping insertion.")
                    return
        except:
            pass
        existing_records = ET0o.objects.filter(i=i)
        if existing_records.exists():
            if existing_records.count() > 1:
                # if there are more than one record with the same value of "i", delete all but the last one
                existing_records[:-1].delete()
                print(f"Removed {existing_records.count() - 1} duplicate records with i={i} from the database.")
            else:
                # if there's only one record with the same value of "i", skip the insertion and print a message
                print(f"A record with i={i} already exists in the database. Skipping insertion.")
                return
    if ss[0] == "8":
        print(ss)
    if ss[0] == "2":
        id_dev = ss[0]
        temp = ss[1]
        hum = ss[2]
        ec = ss[3]
        sal = ss[4]
        v_batt = ss[5]

        print("ID-Dev :" + str(id_dev))
        print("temp :" + str(temp))
        print("hum :" + str(hum))
        print("ec :" + str(ec))
        print("sal :" + str(sal))
        print("v_batt :" + str(v_batt))
        # now = (datetime.datetime.now()).strftime("%M")
        #
        # if not CapSol.objects.filter(time__minute=now).exists():
        #     print(now)
        s = CapSol.objects.create(devId=id_dev,Temp=temp, Hum=hum,Ec=ec, Sal=sal,Bat=v_batt)
        print(s)

    if ss[0] == "3":
        id_dev = ss[0]
        temp = ss[1]
        hum = ss[2]
        ec = ss[3]
        sal = ss[4]
        v_batt = ss[5]

        print("ID-Dev :" + str(id_dev))
        print("temp :" + str(temp))
        print("hum :" + str(hum))
        print("ec :" + str(ec))
        print("sal :" + str(sal))
        print("v_batt :" + str(v_batt))
        # now = (datetime.datetime.now()).strftime("%M")
        #
        # if not CapSol.objects.filter(time__minute=now).exists():
        #     print(now)
        s = CapSol2.objects.create(devId=id_dev,Temp=temp, Hum=hum,Ec=ec, Sal=sal,Bat=v_batt)
        print(s)
    if ss[0][-1] == "1":
        id_dev = ss[0][-1]
        batt = ss[1]
        vite = ss[2]
        ray = ss[3]
        temp = ss[4]
        hum = ss[5]
        plo = ss[6]
        alt = ss[7]
        pr = ss[8]
        d = ss[9]
        i = ss[10]
        print("ID-Dev :" + str(id_dev))
        print("temp :" + str(temp))
        print("hum :" + str(hum))
        print("ray :" + str(ray))
        print("vite :" + str(vite))
        print("plo :" + str(plo))

        print("batt :" + str(batt))
        print("id : ",i)
        batterie = round(float(batt),2)
        print("batterie : ",batterie)
        if ss[5] != "0":
            try:
                if not Data.objects.filter(i=i).exists():
                    Data.objects.create(ID_Device=id_dev, Temp=temp, Hum=hum, Ray=ray, Wind_Speed=vite, Rain=plo,
                                        Bat=batterie, alt=alt, pr=pr, d=d,i=i)
                    print("created!!!")
                else:
                    print(f"A record with i={i} already exists in the database. Skipping insertion.")
                existing_records = Data.objects.filter(i=i)
                print("number record ws :",existing_records.count())
                if existing_records.exists():
                    if existing_records.count() > 1:
                        # if there are more than one record with the same value of "i", delete all but the last one
                        existing_records[:-1].delete()
                        print(f"Removed {existing_records.count() - 1} duplicate records with i={i} from the database.")
                    else:
                        # if there's only one record with the same value of "i", skip the insertion and print a message
                        print(f"A record with i={i} already exists in the database. Skipping insertion.")
                        return
                print("__________________________________WS created________________________________")
            except Exception as e:
                print(" error WS :", e)

        existing_records = Data.objects.filter(i=i)
        if existing_records.exists():
            if existing_records.count() > 1:
                # if there are more than one record with the same value of "i", delete all but the last one
                existing_records[:-1].delete()
                print(f"Removed {existing_records.count() - 1} duplicate records with i={i} from the database.")
            else:
                # if there's only one record with the same value of "i", skip the insertion and print a message
                print(f"A record with i={i} already exists in the database. Skipping insertion.")
                return
    if ss[0][-1] == "9":
        id = ss[0][-1]
        batt = ss[3]
        print("batterie vanne ", batt)
        batvanne.objects.create(bat=batt)
        print("created batterie vanne !!!")


client = mqtt.Client()
# client.username_pw_set(username="opensnz", password="opensnz")
client.connect("broker.hivemq.com", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client2 = mqtt.Client()
# client.username_pw_set(username="opensnz", password="opensnz")
client2.connect("test.mosquitto.org", 1883, 60)

client2.on_connect = on_connect
client2.on_message = on_message
# client.reinitialise()

client.loop_start() #do not disconnect
client2.loop_start()

# def save(self, commit=False, *args, **kwargs):
#     msg=self.onoff
# # msg = vanne.save(self=vanne)
#     print(msg)
# # msg = input("Enter your message:")
#     client.publish("vanne", str(msg))
#     client.loop_stop()