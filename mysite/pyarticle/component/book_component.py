# coding:UTF-8
from pyarticle.models import Book
from pyarticle.models import Chapter
from pyarticle.models import Section


class BookComponent:
    def __init__(self, request, book_id):
        self.book = Book.objects.get(id=book_id)
        # ページ数取得
        self.total_page = self.__get_pages()

    """
    チャプターリストを取得する
    """
    def get_chapter_list(self):
        chapters = Chapter.objects.filter(book=self.book).order_by('order')
        return chapters

    """
    チャプターを取得する
    """
    def get_chapter(self, chapter_id):
        return Chapter.objects.get(id=chapter_id)

    def get_section(self, section_id):
        return Section.objects.get(id=section_id)


    """
    本のページ数を取得する
    """
    def __get_pages(self):
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
    def get_page(self, page):
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






