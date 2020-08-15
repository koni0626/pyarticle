from .component.book_component import BookComponent
from .models import Book, Profile, Comment
from .utils import custom_render, get_user
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
    user = get_user(request.user)
    # マイページには自分の投稿記事とプロフィールを表示する
    book_records = Book.objects.filter(user=user).order_by('create_date').reverse().all()
    # 本全体のアクセス数をカウントする
    books = []
    for book in book_records:
        print(book.id)
        bc = BookComponent(book.id)
        acc = bc.get_book_access_count()
        books.append([book, acc])

    profile = Profile.objects.filter(user=user).first()
    if profile is None:
       profile = Profile()

    # コメント回収
    comments = []
    for book in books:
        book = book[0]
        records = Comment.objects.filter(book=book.id).order_by('update_date').reverse().all()
        if records is not None:
            for record in records:
                comments.append(record)

    data = {'books': books, 'profile': profile, 'comments': comments}
    return custom_render(request, 'pyarticle/admin/mypage/index.html', data)

