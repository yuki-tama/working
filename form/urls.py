# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.form),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.kakikomi, name='kakikomi'),
]
