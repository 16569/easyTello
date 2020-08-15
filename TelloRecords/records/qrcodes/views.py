import json
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import QR

def list_records(request):
    qr = QR.objects.all()
    context = {
        'title': 'QRList',
        'qrcodes': qr
    }
    template = loader.get_template('qrcodes/list_qrcodes.html')
    return HttpResponse(template.render(context, request))

@ensure_csrf_cookie
def receive(request):

    if request.method == 'GET':
        return JsonResponse({})

    # JSON文字列
    datas = json.loads(request.body)
    receive_qr = datas["param1"]

    try:
        qr = QR.objects.get(qr_code=receive_qr)
        #qr.record_id = request.POST['record_id']
        #qr.qr_code = request.POST['qr_code']
        qr.is_done = "1"
        qr.save()
    except QR.DoesNotExist:
        new_id = QR.objects.count() + 1
        new_qr = QR(record_id=new_id, qr_code=receive_qr, is_done="1")
        new_qr.save()

    # JSONに変換して戻す
    ret = {"data": "param1:" + datas["param1"]}
    return JsonResponse(ret)
