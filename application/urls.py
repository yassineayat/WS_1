from django.urls import path

from application import views

urlpatterns = [
    path('', views.home,name="home"),
    path('Chart/', views.chart,name="chart"),
    path('Charthum/', views.charthum,name="charthum"),
    path('Chartsal/', views.chartsal, name="chartsal"),
    path('Chartec/', views.chartec, name="chartec"),
    path('Chartbat/', views.chartbat, name="chartbat"),
    path('data/', views.weatherS,name="data"),
    path('wso/', views.wsopen,name="wso"),
    #Temperature charts
    path('24h/', views.dash,name="acc"),
    path('3jrs/', views.data3,name="3jracc"),
    path('7jrs/', views.data7,name="7jracc"),
    path('15jrs/', views.data15,name="15jracc"),
    ##humidité
    path('h24h/', views.hum1,name="hacc"),
    path('h3jrs/', views.hum3,name="h3jracc"),
    path('h7jrs/', views.hum7,name="h7jracc"),
    path('h15jrs/', views.hum15,name="h15jracc"),
    ##vitesse
    path('v24h/', views.vit1,name="vacc"),
    path('v3jrs/', views.vit3,name="v3jracc"),
    path('v7jrs/', views.vit7,name="v7jracc"),
    path('v15jrs/', views.vit15,name="v15jracc"),

    #rayonnement
    path('r24h/', views.ray1,name="racc"),
    path('r3jrs/', views.ray3,name="r3jracc"),
    path('r7jrs/', views.ray7,name="r7jracc"),
    path('r15jrs/', views.ray15,name="r15jracc"),

    #pluvieu
    path('p24h/', views.plu1,name="pacc"),
    path('p3jrs/', views.plu3,name="p3jracc"),
    path('p7jrs/', views.plu7,name="p7jracc"),
    path('p15jrs/', views.plu15,name="p15jracc"),

    #batterie
    path('b24h/', views.bat1,name="bacc"),
    path('b3jrs/', views.bat3,name="b3jracc"),
    path('b7jrs/', views.bat7,name="b7jracc"),
    path('b15jrs/', views.bat15,name="b15jracc"),
    #et0
    path('et/', views.et,name="et"),
    path('et0/', views.et0,name="et0"),

    #fwi
    path('fwi/', views.fwi0, name="fwi"),

    #temperature sol
    path('st24h/', views.tsol1,name="tsacc"),
    path('st3jrs/', views.tsol3,name="ts3acc"),
    path('st7jrs/', views.tsol7,name="ts7acc"),
    path('st15jrs/', views.tsol15,name="ts15acc"),

    path('2st24h/', views.tsol21,name="2tsacc"),
    path('2st3jrs/', views.tsol23,name="2ts3acc"),
    path('2st7jrs/', views.tsol27,name="2ts7acc"),
    path('2st15jrs/', views.tsol215,name="2ts15acc"),
    #humidite dsol
    path('sh24h/', views.hsol1,name="hsacc"),
    path('sh3jrs/', views.hsol3,name="hs3acc"),
    path('sh7jrs/', views.hsol7,name="hs7acc"),
    path('sh15jrs/', views.hsol15,name="hs15acc"),

    path('2sh24h/', views.hsol21, name="2hsacc"),
    path('2sh3jrs/', views.hsol23, name="2hs3acc"),
    path('2sh7jrs/', views.hsol27, name="2hs7acc"),
    path('2sh15jrs/', views.hsol215, name="2hs15acc"),
    #salinité
    path('ss24h/', views.ssol1, name="ssacc"),
    path('ss3jrs/', views.ssol3, name="ss3acc"),
    path('ss7jrs/', views.ssol7, name="ss7acc"),
    path('ss15jrs/', views.ssol15, name="ss15acc"),

    path('2ss24h/', views.ssol21, name="2ssacc"),
    path('2ss3jrs/', views.ssol23, name="2ss3acc"),
    path('2ss7jrs/', views.ssol27, name="2ss7acc"),
    path('2ss15jrs/', views.ssol215, name="2ss15acc"),
    #EC
    path('es24h/', views.esol1, name="esacc"),
    path('es3jrs/', views.esol3, name="es3acc"),
    path('es7jrs/', views.esol7, name="es7acc"),
    path('es15jrs/', views.esol15, name="es15acc"),

    path('2es24h/', views.esol21, name="2esacc"),
    path('2es3jrs/', views.esol23, name="2es3acc"),
    path('2es7jrs/', views.esol27, name="2es7acc"),
    path('2es15jrs/', views.esol215, name="2es15acc"),
    #batterie sol
    path('bs24h/', views.bsol1, name="bsacc"),
    path('bs3jrs/', views.bsol3, name="bs3acc"),
    path('bs7jrs/', views.bsol7, name="bs7acc"),
    path('bs15jrs/', views.bsol15, name="bs15acc"),

    path('2bs24h/', views.bsol21, name="2bsacc"),
    path('2bs3jrs/', views.bsol23, name="2bs3acc"),
    path('2bs7jrs/', views.bsol27, name="2bs7acc"),
    path('2bs15jrs/', views.bsol215, name="2bs15acc"),
]
