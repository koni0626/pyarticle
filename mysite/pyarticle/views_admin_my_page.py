from datetime import date

from django.db.models import Count

from .component.book_component import BookComponent
from .models import Book, Profile, Comment, AccessLog
from .utils import custom_render, get_user
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login/')
def index(request):
    user = get_user(request.user)
    # マイページには自分の投稿記事とプロフィールを表示する
    book_records = Book.objects.filter(user=user).order_by('create_date').reverse().all()
    # 本全体のアクセス数をカウントする
    books = []
    for book in book_records:
        bc = BookComponent(book.id)
        acc = bc.get_book_access_count()
        books.append(bc.book_info())

    profile = Profile.objects.filter(user=user).first()
    if profile is None:
       profile = Profile()

    # コメント回収
    comments = []
    for book in books:
        book = book['book']
        records = Comment.objects.filter(book=book.id).order_by('update_date').reverse().all()
        if records is not None:
            for record in records:
                comments.append(record)

    # ログ回収
    #logs = AccessLog.objects.filter(user=user).order_by('id').reverse().all()[:100]
    summaries = AccessLog.objects.values('book').filter(user=user, create_date__icontains=date.today()).annotate(count=Count('book')).order_by('count').reverse()
    for summary in summaries:
        book_id = summary['book']
        bc = BookComponent(book_id)
        summary['book'] = bc.book.title

    my_book = True#bc.is_my_book(request.user)
    data = {'books': books, 'profile': profile, 'comments': comments, 'summaries': summaries, 'my_book': my_book}
    return custom_render(request, 'pyarticle/admin/mypage/index.html', data)

