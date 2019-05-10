from django.urls import path
from . import views

urlpatterns = [
    path('', views.FetchInput, name='FetchInput'),
]
