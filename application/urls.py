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
]
