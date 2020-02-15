from django.shortcuts import render
from django.conf import settings
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

    SITE_URL = "{0}://{1}".format(request.scheme, request.get_host())
    record = {'site_name': site_name, 'description': description, 'site_image': url, 'SITE_URL': SITE_URL}
    record.update(data)
    return render(request, template, record)


def custom_admin_render(request, template, data):
    # サイトの名前と説明を毎回呼び出す。もっといい方法はないものか？
    try:
        site_name = SiteParams.objects.get(param='admin_site_name').value
        description = SiteParams.objects.get(param='admin_site_description').value
        SITE_URL = "{0}://{1}".format(request.scheme, request.get_host())
        record = {'site_name': site_name, 'description': description, 'SITE_URL': SITE_URL}
        record.update(data)
    except:
        record = {'site_name': "", 'description': "", 'SITE_URL': ""}
    return render(request, template, record)
