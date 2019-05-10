# from django.shortcuts import render
# from django.http import HttpResponse
#
# def form(request):
#     d = {
#         "scenario" : request.POST.get("scenario"),
#         "name1" : request.POST.get("name1"),
#         "role1" : request.POST.get("role1"),
#     }
#     return render(request, 'form/form.html', d)
from django.shortcuts import render
from django.http import HttpResponse
from form.forms import KakikomiForm

def kakikomi(request):
    if request.method == 'POST':
        f = KakikomiForm(request.POST)
    else:
        f = KakikomiForm()
    return render(
        request,
        'form/form.html',
        {'form1': f} )
