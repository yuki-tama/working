# from django.shortcuts import render
#
# # Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from keijiban.forms import KakikomiForm

def analyse(request):
    content = ScriptForm()
    return HttpResponse(content)
