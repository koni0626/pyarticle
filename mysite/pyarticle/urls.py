from django.urls import path
from . import views
from . import views_admin
from . import views_admin_book
from . import views_admin_chapter
from . import views_admin_section
from . import views_admin_category
from . import views_admin_title
from . import views_accounts
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views_accounts.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="pyarticle/account/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('book/<int:book_id>/<int:page>', views.book, name='disp_book'),
    path('chapter/<int:book_id>/<int:chapter_id>', views.chapter, name='disp_chapter'),
    path('admin/', views_admin.index, name='admin'),
    path('admin/book/', views_admin_book.index, name='book'),
    path('admin/book/add/', views_admin_book.add_book, name='add_book'),
    path('admin/book/edit/<int:book_id>', views_admin_book.edit_book, name='edit_book'),
    path('admin/book/save/<int:book_id>', views_admin_book.save_book, name='save_book'),
    path('admin/book/delete/<int:book_id>', views_admin_book.delete_book, name='delete_book'),
    path('admin/chapter/<int:book_id>', views_admin_chapter.index, name='chapter'),
    path('admin/chapter/add/<int:book_id>', views_admin_chapter.add_chapter, name='add_chapter'),
    path('admin/chapter/edit/<int:book_id>/<int:chapter_id>', views_admin_chapter.edit_chapter, name='edit_chapter'),
    path('admin/chapter/delete/<int:book_id>/<int:chapter_id>', views_admin_chapter.delete_chapter, name='delete_chapter'),
    path('admin/chapter/save/<int:book_id>/<int:chapter_id>', views_admin_chapter.save_chapter, name='save_chapter'),
  #  path('section/<int:book_id>/<int:chapter_id>', views_section.index, name='section'),
    path('admin/section/add/<int:book_id>/<int:chapter_id>', views_admin_section.add_section, name='add_section'),
    path('admin/section/edit/<int:book_id>/<int:chapter_id>/<int:section_id>', views_admin_section.edit_section, name='edit_section'),
    path('admin/section/save/<int:book_id>/<int:chapter_id>/<int:section_id>', views_admin_section.save_section, name='save_section'),
    path('admin/section/delete/<int:book_id>/<int:chapter_id>/<int:section_id>', views_admin_section.delete_section, name='delete_section'),
    path('admin/section_image/save/<int:book_id>/<int:chapter_id>/<int:section_id>/<int:image_id>', views_admin_section.save_section_image, name='save_section_image'),
    path('admin/category/', views_admin_category.index, name='category'),
    path('admin/category/add/', views_admin_category.add_category, name='add_category'),
    path('admin/category/edit/<int:category_id>', views_admin_category.edit_category, name='edit_category'),
    path('admin/category/save/<int:category_id>', views_admin_category.save_category, name='save_category'),
    path('admin/category/delete/<int:category_id>', views_admin_category.delete_category, name='delete_category'),

    path('admin/title/edit', views_admin_title.edit_title, name='edit_title'),
    path('admin/title/save', views_admin_title.save_title, name='save_title'),

]