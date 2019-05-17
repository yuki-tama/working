from django.shortcuts import render
from django.http import HttpResponse
from form.forms import InputScenario

def FetchInput(request):
    if request.method == 'POST':
        f = InputScenario(request.POST)
    else:
        f = InputScenario()
    return render(
        request,
        'form/form.html',
        {'form1': f}
    )
