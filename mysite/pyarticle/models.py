from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
import uuid
import os
# Create your models here.


def get_book_image_path(self, filename):
    """カスタマイズした画像パスを取得する.

    :param self: インスタンス (models.Model)
    :param filename: 元ファイル名
    :return: カスタマイズしたファイル名を含む画像パス
    """
    prefix = 'cover/'
    if not os.path.exists(prefix):
        os.makedirs(prefix)

    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


def get_profile_image_path(self, filename):
    """カスタマイズした画像パスを取得する.

    :param self: インスタンス (models.Model)
    :param filename: 元ファイル名
    :return: カスタマイズしたファイル名を含む画像パス
    """
    prefix = 'profile/'
    if not os.path.exists(prefix):
        os.makedirs(prefix)

    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


def get_section_image_path(self, filename):
    """カスタマイズした画像パスを取得する.

    :param self: インスタンス (models.Model)
    :param filename: 元ファイル名
    :return: カスタマイズしたファイル名を含む画像パス
    """
    prefix = 'section/'
    if not os.path.exists(prefix):
        os.makedirs(prefix)

    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


def get_header_image_path(self, filename):
    """カスタマイズした画像パスを取得する.

    :param self: インスタンス (models.Model)
    :param filename: 元ファイル名
    :return: カスタマイズしたファイル名を含む画像パス
    """
    prefix = 'header/'
    if not os.path.exists(prefix):
        os.makedirs(prefix)

    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to=get_profile_image_path,
                              null=True,
                              verbose_name="プロフィール画像")

    site = models.CharField(max_length=256,
                             null=True,
                             verbose_name="サイト/ブログ",
                             help_text="サイト/ブログ")

    intro = models.CharField(max_length=1024,
                             null=True,
                             verbose_name="自己紹介",
                             help_text="自己紹介")

    twitter = models.CharField(max_length=256,
                             null=True,
                             verbose_name="ツイッターID",
                             help_text="ツイッターID")

    wallet = models.CharField(max_length=1024,
                              null=True,
                              verbose_name="NEMの振込先",
                              help_text="NEMの振込先")

    def get_form_param(self):
        return {'image': self.image, 'site': self.site, 'twitter': self.twitter, 'intro': self.intro, 'wallet': self.wallet}


class SiteParams(models.Model):
    """
    サイト情報
    """
    param = models.CharField(max_length=256,
                             null=False,
                             verbose_name="パラメーター名",
                             help_text="パラメーター名")

    value = models.CharField(max_length=1024,
                             verbose_name="値",
                             help_text="パラメーターの値")

    image = models.ImageField(upload_to=get_header_image_path,
                              null=True,
                              verbose_name="ヘッダ画像")

    def __str__(self):
        return self.param


class Category(models.Model):
    """
    カテゴリ情報
    """
    category_name = models.CharField(max_length=256,
                                     null=False,
                                     unique=True,
                                     verbose_name="カテゴリの名前")

    create_date = models.DateTimeField(auto_now_add=True,
                                       null=True,
                                       verbose_name="作成日")

    update_date = models.DateTimeField(auto_now=True,
                                       null=True,
                                       verbose_name="更新日")

    def __str__(self):
        return self.category_name


class Book(models.Model):
    """
    本の情報
    """
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=256,
                             null=False,
                             unique=True,
                             verbose_name="タイトル")

  #  author = models.CharField(max_length=256,
   #                           verbose_name="作者名")

    description = models.CharField(max_length=512,
                                   verbose_name="説明")

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 verbose_name="カテゴリー",
                                 help_text="カテゴリー")

    good_count = models.IntegerField(default=0,
                                     verbose_name="いいね",
                                     help_text="いいね")

    access_count = models.IntegerField(default=0,
                                       verbose_name="表示回数",
                                       help_text="表示回数")

    image = models.ImageField(upload_to=get_book_image_path,
                              null=True,
                             verbose_name="表紙画像")

    create_date = models.DateTimeField(auto_now_add=True,
                                       null=True,
                                       verbose_name="作成日")

    update_date = models.DateTimeField(auto_now=True,
                                       null=True,
                                       verbose_name="更新日")

    def __str__(self):
        return self.title

class Chapter(models.Model):
    """
    章の情報。見出し。
    """
    #class Meta:
    #    unique_together = ('book', 'order')

    chapter = models.CharField(max_length=256,
                               null=False,
                               unique=False,
                               default="未設定",
                               verbose_name="章")

    order = models.IntegerField(default=1, null=False)

    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             null=False,
                             verbose_name="関連する本",
                             help_text="関連する本")

    access_count = models.IntegerField(default=0,
                                       verbose_name="表示回数",
                                       help_text="表示回数")

    create_date = models.DateTimeField(auto_now_add=True,
                                       null=True,
                                       verbose_name="作成日")

    update_date = models.DateTimeField(auto_now=True,
                                       null=True,
                                       verbose_name="更新日")

    def __str__(self):
        return self.chapter


class Section(models.Model):
    """
    見出しごとの節。本文が入る。
    """
    chapter = models.ForeignKey(Chapter,
                                on_delete=models.CASCADE,
                                null=False,
                                verbose_name="章",
                                help_text="章")

    order = models.IntegerField(default=1,
                                verbose_name="表示する順番")

    text = models.TextField(null=False,
                            verbose_name="コメント")

    access_count = models.IntegerField(default=0,
                                       verbose_name="アクセス数")

    create_date = models.DateTimeField(auto_now_add=True,
                                       null=True,
                                       verbose_name="作成日")

    update_date = models.DateTimeField(auto_now=False,
                                       null=True,
                                       verbose_name="更新日")

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    コメント。本についてコメントが残せる。
    """
    text = models.TextField()

    mail = models.CharField(max_length=256,
                            null=True,
                            verbose_name="メールアドレス",
                            help_text="メールアドレス")

    name = models.CharField(max_length=32,
                            null=True,
                            verbose_name="名前",
                            help_text="名前")

    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             null=False,
                             verbose_name="コメントする本",
                             help_text="コメントする本")

    create_date = models.DateTimeField(auto_now_add=True,
                                       null=True,
                                       verbose_name="作成日")

    update_date = models.DateTimeField(auto_now=True, null=True,
                                       verbose_name="更新日")

    def __str__(self):
        return self.text
