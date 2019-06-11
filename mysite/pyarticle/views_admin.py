from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Book
from .models import Chapter
from .utils import custom_admin_render
from . import forms
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
    records = Book.objects.order_by('id').reverse().all()
    data = {'book_records': records}
    return custom_admin_render(request, 'pyarticle/admin/index.html', data)

