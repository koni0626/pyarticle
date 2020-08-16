# coding:UTF-8
import time
import glob
import os

from django.utils import timezone

from pyarticle.models import Book, User, Profile
from pyarticle.models import Chapter
from pyarticle.models import Section
from django.db.models import Sum

from pyarticle.forms import AttachFileForm
from pyarticle.forms import CommentForm



class BookComponent:
    """
    本に関するクラス
    """
    def __init__(self, book_id):
        self.book_id = book_id
        self.book = Book.objects.get(id=book_id)
        self.title = self.book.title
        self.description = self.book.description
        self.image = self.book.image
        self.attach_file_form = AttachFileForm()
        self.comment_form = CommentForm()
        self.profile = Profile.objects.filter(user=self.book.user).first()
        if self.profile is None:
            Profile(user=self.book.user).save()

    def is_your_book(self, username):
        user = User.objects.filter(username=username).first()
        if user is None:
            return False

        if self.book.user == user:
            return True

        return False

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_image(self):
        return self.image

    def get_chapter_list(self):
        """
        チャプターリストを取得する
        :return:チャプターのリスト
        """
        chapters = Chapter.objects.filter(book=self.book).order_by('order')
        return chapters

    def get_chapter_in_section(self, chapter):
        sub_chapter_list = []
        records = Section.objects.filter(chapter=chapter).order_by('order')

        for record in records:
            text = record.text
            lines = text.split('\n')
            id = 0
            skip = False
            for line in lines:
                if len(line) >= 3 and line[0:3] == "```":
                    if skip:
                        skip = False
                    else:
                        skip = True
                    continue

                if skip == False and len(line) > 2:
                    top = line[0:2]
                    if top == "# ":
                        sub_chapter = line[2:]
                        page = self.get_page(record.id)
                        sub_chapter_list.append([sub_chapter, id, page])
                        id += 1
        return sub_chapter_list

    def get_page_count(self):
        """
        本のページ数を取得する
        :return: ページ数
        """
        page_num = 0
        chapters = self.get_chapter_list()
        if len(chapters) != 0:
            for chapter in chapters:
                sections = Section.objects.filter(chapter=chapter).order_by('order')
                page_num += len(sections)
        return page_num

    def get_chapter_and_section(self, page):
        """
        ページ番号のセクションとチャプターを取得する
        :param page: 取得したいページ番号
        :return: チャプターとセクション
        """
        rtn_chapter = None
        rtn_section = None
        count = 1
        chapters = Chapter.objects.filter(book=self.book).order_by('order')
        if len(chapters) != 0:
            for chapter in chapters:
                sections = Section.objects.filter(chapter=chapter).order_by('order')
                for section in sections:
                    if count == page:
                        rtn_chapter = chapter
                        rtn_section = section
                        break
                    else:
                        count += 1

                if rtn_chapter != None:
                    break

        return rtn_chapter, rtn_section

    def create_empty_book(self):
        """
        チャプターとセクションの空を作成する
        :return:なし
        """
        # 空のチャプター生成
        chapter = Chapter(order=1,
                          book=Book.objects.get(id=self.book.id))
        chapter.save()

        # 空のセクション生成
        section = Section(text="",
                          order=1,
                          update_date=timezone.now(),
                          chapter=Chapter.objects.get(id=chapter.id))
        section.save()

    def is_exists_chapters(self):
        """
        本にチャプターがあるか調べる
        :return: 存在する場合True，存在しない場合False
        """
        ret = True
        try:
            Chapter.objects.filter(book_id=self.book.id)
        except Section.DoesNotExist:
            ret = False

        return ret

    def get_page(self, section_id):
        """
        セクションIDに該当するページ番号を返却する
        :param section_id:ページ番号を取得したいセクションのID
        :return:ページ番号
        """
        page = 1
        find = False
        chapters = Chapter.objects.filter(book=self.book).order_by('order')
        if len(chapters) != 0:
            for chapter in chapters:
                sections = Section.objects.filter(chapter=chapter).order_by('order')
                for section in sections:
                    if section_id == section.id:
                        find = True
                        break
                    else:
                        page += 1

                if find == True:
                    break
        return page

    def get_chapter_top_page(self, chapter_id):
        """
        チャプターのトップページとなるセクションを取得する
        :param chapter_id:チャプターID
        :return:ページ番号
        """
        page = 1
        find = False
        chapters = Chapter.objects.filter(book=self.book).order_by('order')
        if len(chapters) != 0:
            for chapter in chapters:
                if chapter_id == chapter.id:
                    break
                else:
                    sections = Section.objects.filter(chapter=chapter).order_by('order')
                    page += len(sections)
        return page

    @staticmethod
    def delete_chapter(chapter_id):
        """
        チャプターを削除する
        :param chapter_id:削除するチャプターのID
        :return:なし
        """
        Chapter.objects.filter(id=chapter_id).delete()

    @staticmethod
    def delete_section(section_id):
        """
        セクションを削除する
        :param section_id:セクションID
        :return:なし
        """
        Section.objects.filter(id=section_id).delete()

    @staticmethod
    def is_exists_chapter_section(chapter_id):
        """
        チャプターが存在する場合はTrue、存在しない場合はFalseを返す
        :param chapter_id:チェックするチャプターID
        :return:存在する場合True、存在しない場合Falseを返す
        """
        ret = True
        try:
            # もし該当するチャプターのセクションが全部なくなっていたら、
            # 一つだけ空のセクションを作成する
            Section.objects.get(chapter=chapter_id)
        except Section.DoesNotExist:
            ret = False

        return ret

    @staticmethod
    def create_section(chapter_id, text, order):
        """
        セクションを作成し、作成したセクションIDを返す
        :param chapter_id:作成するセクションが所属するチャプターID
        :param text:セクションの内容
        :param order:順番(未使用)
        :return:セクションID
        """
        section = Section(text=text,
                          order=order,
                          update_date=timezone.now(),
                          chapter=Chapter.objects.get(id=chapter_id))
        section.save()

        return section.id

    @staticmethod
    def update_section(section_id, chapter_id, text, order):
        """
        セクションを更新する
        :param section_id:更新するセクションのID
        :param chapter_id: セクションに紐づくチャプターのID
        :param text: セクションの内容
        :param order: セクションの順番
        :return:なし
        """
        section = Section.objects.get(id=section_id)
        section.text = text
        section.order = order
        section.update_date = timezone.now()
        section.chapter = Chapter.objects.get(id=chapter_id)
        section.save()

    def search(self, key_word):
        """
        本全体を検索する(現時点では未使用。Viewクラスに定義している。
        :param key_word: 検索する単語
        :return:次の形式のリストを返す[本の名前, 見つかった文字列, 本のID, ページ番号]
        """
        results = []
        book_id = self.book.id
        title = self.book.title
        page = 1

        description = self.book.description
        # 本のタイトルで検索する
        title_records = Book.objects.filter(title__contains=key_word)
        if len(title_records) > 0:
            results.append([title, description, book_id, page])

        # 本の説明を検索する
        description_records = Book.objects.filter(description__icontains=key_word)
        if len(description_records) > 0:
            results.append([title, description, book_id, page])

        # 見出しを検索する
        chapter_records = Chapter.objects.filter(chapter__icontains=key_word)
        if len(chapter_records) > 0:
            for chapter_record in chapter_records:
                chapter = chapter_record.chapter
                page = self.get_chapter_top_page(chapter_record.id)
                results.append([chapter, chapter, book_id, page])

        # 各ページを検索する
        section_records = Section.objects.filter(text__icontains=key_word)
        if len(section_records) > 0:
            for section_record in section_records:
                text = section_record.text
                page = self.get_page(section_record.id)
                results.append([text, text, book_id, page])

        return results

    def swap_chapter(self, chapter_id, vector=True):
        # チャプター一覧を取得して、orderで降順にソートする
        if vector:
            chapter_records = Chapter.objects.filter(book=self.book).order_by('order')
        else:
            chapter_records = Chapter.objects.filter(book=self.book).order_by('-order')
        prev_chapter = None
        now_chapter = None
        for chapter in chapter_records:
            if chapter.id == chapter_id:
                now_chapter = chapter
                break
            # ひとつ前を検索する
            prev_chapter = chapter

        if now_chapter != None and prev_chapter != None:
            tmp_order = now_chapter.order
            now_chapter.order = prev_chapter.order
            prev_chapter.order = tmp_order
            Chapter.save(now_chapter)
            Chapter.save(prev_chapter)

    def update_access_count(self, request, page):
        session_name = "{}_{}_access".format(self.book_id, page)
        access_session_name = "{}_{}_access_date".format(self.book_id, page)
        is_timeout = False
        now_time = time.time()
        if access_session_name in request.session:

            old_time = request.session[access_session_name]
            if now_time - old_time < 86400.:
                # 24時間経過していないからカウントしない
                is_timeout = False
            else:
                request.session[access_session_name] = now_time
                is_timeout = True
        else:
            request.session[access_session_name] = now_time
            # 初めてのアクセスはタイムアウト扱い
            is_timeout = True

        if not request.session.get(session_name, False) or is_timeout:
            _, section = self.get_chapter_and_section(page)
            section.access_count += 1
            Section.save(section)
            request.session[session_name] = True

    def get_book_access_count(self):
        chapter_list = self.get_chapter_list()
        acc = 0
        for chapter in chapter_list:
            record = Section.objects.filter(chapter=chapter).aggregate(Sum('access_count'))
            if 'access_count__sum' in record:
                if record['access_count__sum'] is not None:
                    acc += record['access_count__sum']

        return acc

    @staticmethod
    def update_chapter_order(chapter_id, order):
        chapter = Chapter.objects.get(id=chapter_id)

        chapter.order = order
        Chapter.save(chapter)

    def get_attach_list(self):
        path = 'media/attach/{}/*'.format(self.book_id)
        attach_file_list = []
        file_list = glob.glob(path)
        for file in file_list:
            filename = file.split(os.sep)[-1]
            attach_file_list.append(['/media/attach/{}/{}'.format(self.book_id, filename), filename])

        return attach_file_list

    def is_already_good(self, request):
        session_name = "{}_good".format(self.book_id)
        access_session_name = "{}_good_date".format(self.book_id)
        now_time = time.time()
        if access_session_name not in request.session:
            return False

        old_time = request.session[access_session_name]
        if now_time - old_time >= 86400.:
            # 24時間経過していないからカウントしない
            return False

        return True

    def set_good(self, request):
        session_name = "{}_good".format(self.book_id)
        access_session_name = "{}_good_date".format(self.book_id)
        is_timeout = False
        now_time = time.time()
        if access_session_name in request.session:

            old_time = request.session[access_session_name]
            if now_time - old_time < 86400.:
                # 24時間経過していないからカウントしない
                is_timeout = False
            else:
                request.session[access_session_name] = now_time
                is_timeout = True
        else:
            request.session[access_session_name] = now_time
            # 初めてのアクセスはタイムアウト扱い
            is_timeout = True

        if not request.session.get(session_name, False) or is_timeout:
            self.book.good_count += 1
            self.book.save()
            request.session[session_name] = True

    def get_book_good_count(self):
        return self.book.good_count
