# coding:UTF-8
from pyarticle.models import Book
from pyarticle.models import Chapter
from pyarticle.models import Section


class BookComponent:
    def __init__(self, book_id):
        self.book = Book.objects.get(id=book_id)
        # ページ数取得

    """
    チャプターリストを取得する
    """
    def get_chapter_list(self):
        chapters = Chapter.objects.filter(book=self.book).order_by('order')
        return chapters


    """
    本のページ数を取得する
    """
    def get_page_count(self):
        page_num = 0
        chapters = self.get_chapter_list()
        if len(chapters) != 0:
            for chapter in chapters:
                sections = Section.objects.filter(chapter=chapter).order_by('order')
                page_num += len(sections)
        return page_num

    """
    ページ番号のセクションとチャプターを取得する
    """
    def get_chapter_and_section(self, page):
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

    """
    チャプターとセクションの空を作成する
    """
    def create_empty_book(self):
        # 空のチャプター生成
        chapter = Chapter(order=1,
                          book=Book.objects.get(id=self.book.id))
        chapter.save()

        # 空のセクション生成
        section = Section(text="",
                          order=1,
                          chapter=Chapter.objects.get(id=chapter.id))
        section.save()

    """
    本にチャプターがあるか
    """
    def is_exists_chapter(self):
        ret = True
        try:
            # もし該当するチャプターのセクションが全部なくなっていたら、
            # 一つだけ空のセクションを作成する
            Chapter.objects.get(book_id=self.book.id)
        except Section.DoesNotExist:
            ret = False

        return ret

    """
    セクションIDに該当するページ番号を返却する
    """
    def get_page(self, section_id):
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

    """
    チャプターのトップページとなるセクションを取得する
    """
    def get_chapter_top_page(self, chapter_id):
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

    """
    チャプターを削除する
    """
    def delete_chapter(self, chapter_id):
        Chapter.objects.filter(id=chapter_id).delete()

    """
    セクションを削除する
    """
    def delete_section(self, section_id):
        Section.objects.filter(id=section_id).delete()

    """
    チャプターが存在する場合True，存在しない場合Falseを返す
    """
    def is_exists_chapter(self, chapter_id):
        ret = True
        try:
            # もし該当するチャプターのセクションが全部なくなっていたら、
            # 一つだけ空のセクションを作成する
            Section.objects.get(id=chapter_id)
        except Section.DoesNotExist:
            ret = False

        return ret

    """
    セクションを作成し、作成したセクションIDを返す
    """
    def create_section(self, chapter_id, text, order):
        section = Section(text=text,
                          order=1,
                          chapter=Chapter.objects.get(id=chapter_id))
        section.save()

        return section.id

    """
    セクションを更新する
    """
    def update_section(self, section_id, chapter_id, text, order):
        section = Section.objects.get(id=section_id)
        section.text = text
        section.order = order
        section.chapter = Chapter.objects.get(id=chapter_id)
        section.save()

