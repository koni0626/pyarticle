import os
from PIL import Image
from django.conf import settings


def change_attach_file_permission(book_id, filename):
    """
    添付ファイルのパスを取得する
    :param book_id: 本のID
    :param filename: ファイル名
    :return:
    """
    attach_file_name = settings.MEDIA_ROOT + f'/attach/{book_id}/{filename}'
    os.chmod(attach_file_name, 0o666)

