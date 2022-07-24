from django.db import models
from django.conf.locale.en import formats as en_formats
en_formats.TIME_FORMATS = ['%H:%M:%S']
# Create your models here.
class vanne(models.Model):
    onoff = models.BooleanField(default=False)
    dt=models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.onoff)

    def save(self, *args, **kwargs):
        msg=self.onoff
        print("msg" +str(msg))
        # client.publish("vanne", str(msg))

        import paho.mqtt.client as mqtt

        client = mqtt.Client()
        client.username_pw_set("user", "user")  # authentification
        # client.connect("broker.hivemq.com",1883,60) #connect with EC2 instance on port 8883
        # client.connect("192.168.43.112", 1883, 60)
        client.connect("mqtt.eclipseprojects.io", 1883, 60)
        # msg = input("Enter your message:")
        client.publish("vanne", msg);  # publish the message typed by the user
        # client.disconnect(); #disconnect from server


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


class CapSol2(models.Model):
    devId = models.IntegerField()
    Temp = models.FloatField( null=True)
    Hum = models.FloatField( null=True)
    Ec = models.FloatField( null=True)
    Sal = models.FloatField( null=True)
    Bat = models.FloatField( null=True)
    dt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.devId)


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


class Data(models.Model):
    ID_Device = models.IntegerField()
    Temp = models.FloatField(null=True)
    Hum = models.FloatField(null=True)
    Ray = models.FloatField(null=True)
    Wind_Speed = models.FloatField(null=True)
    Rain = models.FloatField( null=True)
    Wind_Dir = models.CharField(max_length=50,null=True)
    Bat = models.FloatField( null=True)
    Time_Stamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.Time_Stamp)


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