from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import SiteParams
from .utils import custom_admin_render
from . import forms
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def edit_title(request):
    site_name = SiteParams.objects.filter(param="site_name").first().value
    site_description = SiteParams.objects.filter(param="site_description").first().value
    site_image = SiteParams.objects.filter(param="site_image").first().image
    form = forms.SiteTitleForm(initial={'site_name': site_name,
                                        'site_description': site_description,
                                        'image': site_image})

    data = {'title_form': form, 'site_image': site_image}

    return custom_admin_render(request, 'pyarticle/admin/title/title.html', data)


@login_required
def save_title(request):
    if request.method == 'POST':
        form = forms.SiteTitleForm(request.POST, request.FILES)
        if form.is_valid():
            site_name = SiteParams.objects.get(param="site_name")
            site_name.value = form.cleaned_data["site_name"]
            site_name.save()

            site_description = SiteParams.objects.get(param="site_description")
            site_description.value = form.cleaned_data["site_description"]
            site_description.save()

            site_image = SiteParams.objects.get(param="site_image")

            if form.cleaned_data['image']:
                site_image.image = form.cleaned_data['image']
                site_image.save()

        else:
            print("error＝＝＝＝＝＝＝")
        return HttpResponseRedirect(reverse('index'))
