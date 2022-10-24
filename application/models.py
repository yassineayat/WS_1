import datetime

from django.db import models
from django.conf.locale.en import formats as en_formats
en_formats.TIME_FORMATS = ['%H:%M:%S']
# Create your models here.
class vann(models.Model):
    onoff = models.BooleanField(default=False)

    dt=models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.onoff)

    def save(self, *args, **kwargs):
        msg=self.onoff
        super(vann, self).save(*args, **kwargs)

        # client.publish("vanne", str(msg))

        import paho.mqtt.client as mqtt

        client1 = mqtt.Client()
        client = mqtt.Client()
        client1.disconnect()
        client1.connect("broker.hivemq.com", 1883, 80)
        client.connect("broker.hivemq.com", 1883, 80)
        print("..................")
        print("self :", self.onoff)
        if (self.onoff == False):
            client.publish("test", "0")
            print("off")
        elif (self.onoff == True):
            client1.publish("test1","1")  # publish the message typed by the user# publish the message typed by the user
            print("on")
        #client1.disconnect() #disconnect from server


class batvanne(models.Model):
    bat = models.FloatField( null=True)
    dt = models.DateTimeField(auto_now=True, null=True)


class CapSol(models.Model):
    devId = models.IntegerField()
    Temp = models.FloatField( null=True)
    Hum = models.FloatField( null=True)
    Ec = models.FloatField( null=True)
    Sal = models.FloatField( null=True)
    Bat = models.FloatField( null=True)
    time=models.TimeField(auto_now=True)
    dt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.dt)
    # def save(self, *args, **kwargs):
    #     now = datetime.datetime.now()
    #     print("created ...... capteur de sol ",now)


class CapSol2(models.Model):
    devId = models.IntegerField()
    Temp = models.FloatField( null=True)
    Hum = models.FloatField( null=True)
    Ec = models.FloatField( null=True)
    Sal = models.FloatField( null=True)
    Bat = models.FloatField( null=True)
    dt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.dt)


class Ws(models.Model):
    Temperature = models.FloatField( null=True)
    Humidity = models.FloatField( null=True)
    Vent = models.FloatField( null=True)
    Rafale = models.FloatField( null=True)
    Pluv = models.FloatField( null=True)
    Ray = models.FloatField( null=True)
    date = models.DateTimeField(null=True)
    dateRay = models.DateTimeField(null=True)
    def __str__(self):
        return str(self.pk )  +  str(self.date)

class Ray(models.Model):
    Ray = models.FloatField(null=True)
    dateRay = models.DateTimeField(null=True)
    def __str__(self):
        return str(self.Ray)

class Data(models.Model):
    ID_Device = models.IntegerField()
    Temp = models.FloatField(null=True)
    Hum = models.FloatField(null=True)
    Ray = models.FloatField(null=True)
    Wind_Speed = models.FloatField(null=True)
    Rain = models.FloatField(null=True)
    Wind_Dir = models.CharField(max_length=50,null=True)
    Bat = models.FloatField(null=True)
    Time_Stamp = models.DateTimeField(auto_now_add=True)
    diff = models.DurationField(null=True, blank=True)

    def __str__(self):
        return str(self.diff)
    #
    # def save(self, *args, **kwargs):
    #     now = datetime.datetime.now()
    #     x=now.time.strftime("%H:%M:%S")
    #     if not Data.objects.filter(Time_Stamp__date= now.date,Time_Stamp__time=x).exists():
    #         print("not exist ....")
    #
    #     else:
    #         print("data exist ")
    # def save(self, *args, **kwargs):
    #     now = datetime.datetime.now()
    #     print("created ......Weather station ",now)


class ET0(models.Model):
    value = models.FloatField(null=True)
    WSavg = models.FloatField(null=True)
    Tmax = models.FloatField(null=True)
    Tmin = models.FloatField(null=True)
    Hmax = models.FloatField(null=True)
    Hmin = models.FloatField(null=True)
    Raym = models.FloatField(null=True)
    U2 = models.FloatField(null=True)
    Delta = models.FloatField(null=True)
    Time_Stamp = models.DateTimeField(auto_now_add=True)
    dt = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return "ET0: "+str(self.Time_Stamp)

class DataFwi(models.Model):
    ffmc = models.FloatField()
    dmc = models.FloatField()
    dc = models.FloatField()
    isi = models.FloatField()
    bui = models.FloatField()
    fwi = models.FloatField()
    Time_Stamp = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return "FWI = "+str(self.fwi)+" @ "+str(self.Time_Stamp)



class ET0o(models.Model):
    value = models.FloatField(null=True)
    WSavg = models.FloatField(null=True)
    Tmax = models.FloatField(null=True)
    Tmin = models.FloatField(null=True)
    Hmax = models.FloatField(null=True)
    Hmin = models.FloatField(null=True)
    Raym = models.FloatField(null=True)
    U2 = models.FloatField(null=True)
    Delta = models.FloatField(null=True)
    Time_Stamp = models.DateTimeField(auto_now_add=True)
    dt = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return "ET0: "+str(self.value)

    def save(self, *args, **kwargs):
        msg=self.value
        super(ET0o, self).save( *args, **kwargs)
        print("msg" +str(msg))
        # client.publish("vanne", str(msg))

        import paho.mqtt.client as mqtt

        client = mqtt.Client()

        client.connect("broker.hivemq.com", 1883, 80)

        client.publish("et", msg)  # publish the message typed by the user
        print(msg)
        client.disconnect(); #disconnect from server