from django.urls import path

from application import views

urlpatterns = [
    path('', views.home,name="home"),
    path('Chart/', views.chart,name="chart"),
    path('data/', views.weatherS,name="data"),
    path('wso/', views.wsopen,name="wso"),
]
