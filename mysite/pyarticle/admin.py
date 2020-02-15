from django.contrib import admin
from .models import Book
from .models import Category
from .models import Chapter
from .models import Section
from .models import SiteParams
# Register your models here.

admin.site.register(SiteParams)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Section)
