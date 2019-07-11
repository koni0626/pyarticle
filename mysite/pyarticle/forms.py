# coding:UTF-8
from django import forms
from . import models


class BookForm(forms.Form):
    title = forms.CharField(label='タイトル',
                            widget=forms.TextInput(attrs={'size': '100'}))

    author = forms.CharField(label='著者',
                             widget=forms.TextInput(attrs={'size': '100'}))

    description = forms.CharField(label='本の説明',
                                  widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    category = forms.ModelChoiceField(label='カテゴリー',
                                      queryset=models.Category.objects.all())

    image = forms.ImageField(required=False)


class ChapterForm(forms.Form):
    chapter = forms.CharField(label='章',
                              widget=forms.TextInput(attrs={'size': '100'}))

    order = forms.IntegerField(label="順番")


class SectionForm(forms.Form):
    text = forms.CharField(label='本文',
                           widget=forms.Textarea(attrs={'cols': 100, 'rows': 50}))

    order = forms.IntegerField(label="順番")

    image = forms.ImageField(required=False)


class SectionImageForm(forms.Form):
    image = forms.ImageField(required=False)


class CategoryForm(forms.Form):
    category = forms.CharField(label='カテゴリー',
                               widget=forms.TextInput(attrs={'size': '100'}))


class SiteTitleForm(forms.Form):
    image = forms.ImageField(required=False)

    site_name = forms.CharField(label='タイトル',
                                 widget=forms.TextInput(attrs={'size': '100'}))

    site_description = forms.CharField(label='説明',
                                       widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}))