from django.shortcuts import render
from django.http import HttpResponse

def form(request):
    d = {
        "scenario" : request.POST.get("scenario"),
        "name1" : request.POST.get("name1"),
        "role1" : request.POST.get("role1")
    }
    return render(request, 'form/form.html', d)
