from datetime import date
from django.core.paginator import Paginator
from django.db.models import Count, Q

from .component.book_component import BookComponent
from .forms import SearchForm
from .models import Book, Profile, Comment, AccessLog, Chapter
from .utils import custom_render, get_user, search_books
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login/')
def index(request):
    user = get_user(request.user)
    # マイページには自分の投稿記事とプロフィールを表示する
    key_word = ""
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            key_word = search_form.cleaned_data['key_word']

    book_records = Book.objects.filter(Q(user=user), Q(title__contains=key_word)|Q(description__contains=key_word)).order_by('create_date').reverse().all()
    paginator = Paginator(book_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # 本全体のアクセス数をカウントする
    books = []
    for book in page_obj:
        bc = BookComponent(book.id)
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

    my_book = True

    # 検索フォームの作成
    search_form = SearchForm()

    data = {'books': books, 'profile': profile, 'comments': comments, 'summaries': summaries, 'my_book': my_book,
            'search_form': search_form, 'page_obj': page_obj}

    return custom_render(request, 'pyarticle/admin/mypage/index.html', data)

