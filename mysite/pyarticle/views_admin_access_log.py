from .component.book_component import BookComponent
from .models import Book, Profile, Comment, AccessLog
from .utils import custom_render, get_user
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.


@login_required
def index(request):
    user = get_user(request.user)
    # マイページには自分の投稿記事とプロフィールを表示する
    logs = AccessLog.objects.filter(user=user).order_by('id').reverse().all()
    data = {'logs': logs}
    return custom_render(request, 'pyarticle/admin/access_log/index.html', data)

