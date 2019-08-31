from django.shortcuts import render
from django.http import HttpResponse
from .models import SiteParams
# Create your views here.


def custom_render(request, template, data):
    # サイトの名前と説明を毎回呼び出す。もっといい方法はないものか？

    site_name = SiteParams.objects.get(param='site_name').value
    description = SiteParams.objects.get(param='site_description').value
    image = SiteParams.objects.get(param='site_image').image
    try:
        url = image.url
    except:
        url = ""

    record = {'site_name': site_name, 'description': description, 'site_image': url}
    record.update(data)
    return render(request, template, record)


def custom_admin_render(request, template, data):
    # サイトの名前と説明を毎回呼び出す。もっといい方法はないものか？
    try:
        site_name = SiteParams.objects.get(param='admin_site_name').value
        description = SiteParams.objects.get(param='admin_site_description').value

        record = {'site_name': site_name, 'description': description}
        record.update(data)
    except:
        record = {'site_name': "", 'description': ""}
    return render(request, template, record)
