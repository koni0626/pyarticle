# coding:UTF-8
from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class BookForm(forms.Form):
    title = forms.CharField(label='タイトル',
                            widget=forms.TextInput(attrs={'size': '100'}))

    description = forms.CharField(label='本の説明',
                                  widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    category = forms.ModelChoiceField(label='カテゴリー',
                                      queryset=models.Category.objects.all())

    draft = forms.ChoiceField(label='公開/非公開',
                              choices=[(0, "非公開"), (1, "公開")])

    image = forms.ImageField(required=False)

    footer = forms.CharField(label='フッター', required=False,
                             widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    article_type = forms.ChoiceField(label='本形式/日記形式',
                                     choices=[(0, "本形式"), (1, "日記形式")])


class FooterForm(forms.Form):
    footer = forms.CharField(label='フッター', required=False,
                             widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))


class ChapterForm(forms.Form):
    chapter = forms.CharField(label='章',
                              widget=forms.TextInput(attrs={'size': '100'}))

    order = forms.IntegerField(label="順番")


class SectionForm(forms.Form):
    text = forms.CharField(label='本文', required=False, strip=False,
                           widget=forms.Textarea(attrs={'cols': 100, 'rows': 50, "contenteditable":"true"}))

    order = forms.IntegerField(label="順番")

    image = forms.ImageField(required=False)


class AttachFileForm(forms.Form):
    attach_file = forms.FileField(required=False)


class SectionImageForm(forms.Form):
    image = forms.ImageField(required=False)


class CategoryForm(forms.Form):
    category = forms.CharField(label='カテゴリー',
                               widget=forms.TextInput())


class ProfileForm(forms.Form):
    class Meta:
        model = models.Profile
        fields = '__all__'
    image = forms.ImageField(label='アイコン画像', required=False)

    site = forms.CharField(label='サイト/ブログ', required=False,
                           widget=forms.TextInput(attrs={'size': '100'}))

    name = forms.CharField(label='表示名', required=False,
                           widget=forms.TextInput(attrs={'size': '100'}))

    twitter = forms.CharField(label='ツイッターID', required=False,
                              widget=forms.TextInput(attrs={'size': '100'}))

    intro = forms.CharField(label='自己紹介', required=False,
                            widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}))

    nem_address = forms.CharField(label='NEMの振込先アドレス', required=False,
                                  widget=forms.TextInput(attrs={'size': '100'}))

    nem_message = forms.CharField(label='NEM メッセージ', required=False,
                                  widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}))

class SiteTitleForm(forms.Form):
    image = forms.ImageField(required=False)

    site_name = forms.CharField(label='タイトル',
                                 widget=forms.TextInput(attrs={'size': '100', 'class': 'form-control'}))

    site_upload_url = forms.CharField(label='画像の送信先URL',
                                 widget=forms.TextInput(attrs={'size': '100', 'class': 'form-control'}))

    site_description = forms.CharField(label='説明',
                                       widget=forms.Textarea(attrs={'cols': 100, 'rows': 5, 'class': 'form-control'}))

    site_news = forms.CharField(label='お知らせ',
                                widget=forms.Textarea(attrs={'cols': 100, 'rows': 5, 'class': 'form-control'}))

    site_data_sitekey = forms.CharField(label='このサイトキーは、ユーザーに表示するサイトの HTML コードで使用します',
                                 widget=forms.TextInput(attrs={'size': '100', 'class': 'form-control'}))

    site_secret = forms.CharField(label='このシークレット キーは、サイトと reCAPTCHA 間の通信で使用します',
                                 widget=forms.TextInput(attrs={'size': '100', 'class': 'form-control'}))

class SiteHeaderForm(forms.Form):
    image = forms.ImageField(required=False)

    site_name = forms.CharField(label='タイトル',
                                 widget=forms.TextInput(attrs={'size': '100', 'class': 'form-control'}))

    site_description = forms.CharField(label='説明',
                                       widget=forms.Textarea(attrs={'cols': 100, 'rows': 5, 'class': 'form-control'}))

class SiteBookHeaderForm(forms.Form):
    image = forms.ImageField(required=False)


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)


class SearchForm(forms.Form):
    key_word = forms.CharField(label='検索', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))


class CommentForm(forms.Form):
    email = forms.EmailField(
        label='メールアドレス',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレスを入力してください",
        }),
    )

    text = forms.CharField(label='問い合わせ', required=True,
                           widget=forms.Textarea(attrs={'size': '1024',
                                                        'class': 'form-control',
                                                         'placeholder': "お問い合わせの内容は執筆者にだけ通知されます"}))

    name = forms.CharField(label='お名前', required=True,
                           widget=forms.TextInput(attrs={'size': '32',
                                                         'class': 'form-control',
                                                         'placeholder': "お名前を入力してください"}))

