from .models import Book
from .utils import custom_render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
    records = Book.objects.order_by('id').reverse().all()
    data = {'book_records': records}
    return custom_render(request, 'pyarticle/admin/index.html', data)

