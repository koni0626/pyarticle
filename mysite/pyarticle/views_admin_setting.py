from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import SiteParams
from .utils import custom_render
from . import forms
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def edit_setting(request):
    try:
        site_image = SiteParams.objects.filter(param="site_image").first().image
    except:
        site_image = ""

    try:
        site_name = SiteParams.objects.filter(param="site_name").first().value
        site_description = SiteParams.objects.filter(param="site_description").first().value
        site_upload_url = SiteParams.objects.filter(param="upload_url").first().value

        site_data_sitekey = SiteParams.objects.filter(param="data_sitekey").first().value
        site_secret = SiteParams.objects.filter(param="site_secret").first().value
        site_news = SiteParams.objects.filter(param="site_news").first().value

        form = forms.SiteTitleForm(initial={'site_name': site_name,
                                            'site_description': site_description,
                                            'image': site_image,
                                            'site_upload_url': site_upload_url,
                                            'site_secret': site_secret,
                                            'site_data_sitekey': site_data_sitekey,
                                            'site_news': site_news})

        data = {'title_form': form, 'site_image': site_image.url}
    except:
        form = forms.SiteTitleForm()
        data = {'title_form': form, 'site_image': ""}

    return custom_render(request, 'pyarticle/admin/setting/setting.html', data)


@user_passes_test(lambda u: u.is_superuser)
def save_setting(request):
    if request.method == 'POST':
        form = forms.SiteTitleForm(request.POST, request.FILES)
        if form.is_valid():
            site_name = SiteParams.objects.get(param="site_name")
            site_name.value = form.cleaned_data["site_name"]
            site_name.save()

            site_description = SiteParams.objects.get(param="site_description")
            site_description.value = form.cleaned_data["site_description"]
            site_description.save()

            site_url = SiteParams.objects.get(param="upload_url")
            site_url.value = form.cleaned_data["site_upload_url"]
            site_url.save()

            site_data_sitekey = SiteParams.objects.get(param="data_sitekey")
            site_data_sitekey.value = form.cleaned_data["site_data_sitekey"]
            site_data_sitekey.save()

            site_secret = SiteParams.objects.get(param="site_secret")
            site_secret.value = form.cleaned_data["site_secret"]
            site_secret.save()

            site_news = SiteParams.objects.get(param="site_news")
            site_news.value = form.cleaned_data["site_news"]
            site_news.save()

            site_image = SiteParams.objects.get(param="site_image")

            if form.cleaned_data['image']:
                site_image.image = form.cleaned_data['image']
                site_image.save()

        else:
            pass
        return HttpResponseRedirect(reverse('index'))
