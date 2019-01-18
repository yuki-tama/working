from django.urls import path
from keijiban import views

urlpatterns = [
    path('', views.analyse, name='analyse'),
]
