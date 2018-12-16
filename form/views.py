from django.shortcuts import render
from django.http import HttpResponse

def form(request):
    return render(request, 'form/form.html', {})

def arrange_format(req):    # AJAXに答える関数
    import json
    from django.http import HttpResponse, Http404

    if req.method == 'POST':
        scenario = req.POST['scenario']

        response = json.dumps({'scenario':surprise_txt,})  # JSON形式に直して・・

        return HttpResponse(response,mimetype="text/javascript")  # 返す。JSONはjavascript扱いなのか・・

    else:
        raise Http404  # GETリクエストを404扱いにしているが、実際は別にしなくてもいいかも
