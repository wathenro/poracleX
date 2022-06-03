from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('index/',views.mainpage,name='mainpage'),
    path('index/ssrf/',views.get_ssrf,name="ssrf"),
    path('index/identification/',views.get_identification,name="identification")
   
]