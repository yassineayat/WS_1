import datetime

import paho.mqtt.client as mqtt
import django
django.setup()


from application.models import *
# from application.models import vanne


def on_connect(client, userdata, flags, rc):
    #print("Connected with result code " + str(rc)) #notify about established connection
    client.subscribe("message")
    client.subscribe("capteur2")

def on_message(client, userdata, msg):
    ms = msg.payload
    data = str(ms[0: len(ms)])[2:-1]
    # data = str(ms)
    print("Your message:" + data) #display received message
    ss = data.split(' ')
    print(ss)
    if ss[0] == "02":
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
    if ss[0][-1] == "1":
        id_dev = ss[0][-1]
        temp = ss[1]
        hum = ss[2]
        ray = ss[3]
        vite = ss[4]
        plo = ss[5]
        Wind_Dir = ss[6]
        batt = ss[7]
        print("ID-Dev :" + str(id_dev))
        print("temp :" + str(temp))
        print("hum :" + str(hum))
        print("ray :" + str(ray))
        print("vite :" + str(vite))
        print("plo :" + str(plo))
        print("Wind_Dir :" + str(Wind_Dir))
        print("batt :" + str(batt))
        # now = (datetime.datetime.now()).strftime("%M")
        #
        # if not CapSol.objects.filter(time__minute=now).exists():
        #     print(now)
        s = Data.objects.create(ID_Device=id_dev,Temp=temp, Hum=hum,Ray=ray, Wind_Speed=vite,Rain=plo,Wind_Dir=Wind_Dir, Bat=batt)
        print("created!!!")


client = mqtt.Client()

''' replace with username for authentification '''
client.username_pw_set("user","user")

client.connect("broker.hivemq.com", 1883, 60)
# client.connect("10.130.1.210", 1883, 60)
try:
    client.on_connect = on_connect
    client.on_message = on_message
    # client.loop_forever() #do not disconnect

except Exception as e:
    print(e)
    pass







# def save(self, commit=False, *args, **kwargs):
#     msg=self.onoff
# # msg = vanne.save(self=vanne)
#     print(msg)
# # msg = input("Enter your message:")
#     client.publish("vanne", str(msg))
#     client.loop_stop()