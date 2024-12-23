from .models import Book
from .utils import custom_render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login/')
def index(request):
    """
    マイページにアクセスした場合
    :param request:
    :return:
    """
    records = Book.objects.order_by('id').reverse().all()
    data = {'book_records': records}
    return custom_render(request, 'pyarticle/admin/index.html', data)

