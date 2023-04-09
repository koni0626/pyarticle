from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Comment
from .models import Book
from .models import SiteParams
from . import forms
from .utils import custom_render
from django.contrib.auth.decorators import login_required
# Create your views here.


# @login_required(login_url='login/')
def disp_comment(request):
    records = Comment.objects.order_by('id').reverse().all()

    data = {'records': records}
    return custom_render(request, 'pyarticle/admin/comment/index.html', data)


def save_comment(request, book_id, page):
    if request.method == 'POST':
        res = recaptha(request)
        if not res['success']:
            return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

        form = forms.CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            if text.isascii():
                return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))
            else:
                chapter = Comment(mail=form.cleaned_data['email'],
                                  name=form.cleaned_data['name'],
                                  text=form.cleaned_data['text'],
                                  book=Book.objects.get(id=book_id))
                chapter.save()

        return HttpResponseRedirect(reverse('disp_book', args=[book_id, page]))

def recaptha(req):
    import urllib, urllib.request, urllib.parse, json
    recaptcha_response = req.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data_sitekey = SiteParams.objects.get(param='site_secret').value
    values = {
        'secret': data_sitekey, # GOOGLE RECAPTHA SECRET KEY
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode('utf-8'))
    return result