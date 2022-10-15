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
]
