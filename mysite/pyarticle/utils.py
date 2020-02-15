from django.shortcuts import render
from django.conf import settings
from .models import SiteParams
# Create your views here.


def custom_render(request, template, data):
    # サイトの名前と説明を毎回呼び出す。もっといい方法はないものか？

    site_name = SiteParams.objects.get(param='site_name').value
    description = SiteParams.objects.get(param='site_description').value
    image = SiteParams.objects.get(param='site_image').image
    upload_url = SiteParams.objects.get(param='upload_url').value
    try:
        url = image.url
    except:
        url = ""

    record = {'site_name': site_name, 'description': description, 'site_image': url, 'upload_url': upload_url}
    record.update(data)
    return render(request, template, record)

