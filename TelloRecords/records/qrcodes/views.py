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
    receive_qr = datas["qrcode"]
    x = datas["pos_x"]
    y = datas["pos_y"]
    z = datas["pos_z"]

    try:
        qr = QR.objects.get(qr_code=receive_qr)
        #qr.record_id = request.POST['record_id']
        #qr.qr_code = request.POST['qr_code']
        qr.is_done = "1"
        qr.pos_x=x
        qr.pos_y=y
        qr.pos_z=z
        qr.save()
    except QR.DoesNotExist:
        new_id = QR.objects.count() + 1
        new_qr = QR(record_id=new_id, qr_code=receive_qr, is_done="1", pos_x=x, pos_y=y, pos_z=z)
        new_qr.save()

    # JSONに変換して戻す
    ret = {"data": "param1:" + datas["param1"] + ",posx:" + datas["posx"] + ",posy:" + datas["posy"] + ",posz:" + datas["posz"]}
    return JsonResponse(ret)
