from django.urls import path
from . import views, views_admin_my_page, views_admin_access_log, views_admin_book_header
from . import views_admin
from . import views_admin_book
from . import views_admin_chapter
from . import views_admin_section
from . import views_admin_category
from . import views_admin_title
from . import views_admin_comment
from . import views_accounts
from . import views_admin_setting
from . import views_admin_profile
from . import views_admin_game
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),
    path('google2e5390c579ead2bb.html', views.serve_google_html, name='serve_google_html'),
    #path('', views_admin_my_page.index, name='my_page'),

    path('signup/', views_accounts.signup, name='signup'),
    path('login/', views_accounts.login, name='login'),
    #   path('login/', auth_views.LoginView.as_view(template_name="pyarticle/account/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('book_search/', views.search, name='book_search'),

    path('save_attach_file/<int:book_id>/<int:page>', views_admin_book.upload_attach_file, name='save_attach_file'),
    path('save_attach_file/<int:book_id>/<int:page>/<str:filename>', views_admin_book.delete_attach_file, name='delete_attach_file'),

    path('book/<int:book_id>/<int:page>', views.book, name='disp_book'),
    path('chapter/<int:book_id>/<int:chapter_id>', views.chapter, name='disp_chapter'),

    path('set_good/<int:book_id>', views.set_good, name='ajax_set_good'),

  #  path('admin/', views_admin.index, name='admin'),
    path('admin/book/add/', views_admin_book.add_book, name='add_book'),
    path('admin/book/edit/<int:book_id>', views_admin_book.edit_book, name='edit_book'),
    path('admin/book/save/<int:book_id>', views_admin_book.save_book, name='save_book'),
    path('admin/book/delete/<int:book_id>', views_admin_book.delete_book, name='delete_book'),
    path('admin/book/edit_footer/<int:book_id>/<int:section_id>', views_admin_book.edit_footer, name='edit_footer'),
    path('admin/book/save_footer/<int:book_id>/<int:section_id>', views_admin_book.save_footer, name='save_footer'),

    path('admin/chapter/<int:book_id>', views_admin_chapter.index, name='chapter'),
    path('admin/chapter/add/<int:book_id>', views_admin_chapter.add_chapter, name='add_chapter'),
    path('admin/chapter/edit/<int:book_id>/<int:chapter_id>', views_admin_chapter.edit_chapter, name='edit_chapter'),
    path('admin/chapter/delete/<int:book_id>/<int:chapter_id>', views_admin_chapter.delete_chapter, name='delete_chapter'),
    path('admin/chapter/save/<int:book_id>/<int:chapter_id>', views_admin_chapter.save_chapter, name='save_chapter'),
    path('admin/chapter/upper/<int:book_id>/<int:chapter_id>/<int:page>', views_admin_chapter.upper_chapter, name='upper_chapter'),
    path('admin/chapter/under/<int:book_id>/<int:chapter_id>/<int:page>', views_admin_chapter.under_chapter, name='under_chapter'),
    path('admin/chapter/save_line', views_admin_chapter.ajax_save_chapter, name='ajax_save_chapter'),

    #  path('section/<int:book_id>/<int:chapter_id>', views_section.index, name='section'),
    path('admin/section/add/<int:book_id>/<int:chapter_id>', views_admin_section.add_section, name='add_section'),
    path('admin/section/edit/<int:book_id>/<int:chapter_id>/<int:section_id>', views_admin_section.edit_section, name='edit_section'),
    path('admin/section/save/<int:book_id>/<int:chapter_id>/<int:section_id>', views_admin_section.save_section, name='save_section'),
    path('admin/section/delete/<int:book_id>/<int:chapter_id>/<int:section_id>', views_admin_section.delete_section, name='delete_section'),

    path('admin/category/', views_admin_category.index, name='category'),
    path('admin/category/add/', views_admin_category.add_category, name='add_category'),
    path('admin/category/edit/<int:category_id>', views_admin_category.edit_category, name='edit_category'),
    path('admin/category/save/<int:category_id>', views_admin_category.save_category, name='save_category'),
    path('admin/category/save_auto', views_admin_category.ajax_save_category, name='ajax_save_category'),
    path('admin/category/delete/<int:category_id>', views_admin_category.delete_category, name='delete_category'),

    path('admin/title/edit', views_admin_title.edit_title, name='edit_title'),
    path('admin/title/save', views_admin_title.save_title, name='save_title'),

    path('admin/setting/edit', views_admin_setting.edit_setting, name='edit_setting'),
    path('admin/setting/save', views_admin_setting.save_setting, name='save_setting'),

    path('admin/section/image', views_admin_section.upload_image, name='upload_image'),

    path('admin/comment/add/<int:book_id>/<int:page>', views_admin_comment.save_comment, name='save_comment'),
    path('admin/comment/', views_admin_comment.disp_comment, name='disp_comment'),

    path('admin/profile/edit', views_admin_profile.edit, name='profile_edit'),
    path('admin/mypage', views_admin_my_page.index, name='my_page'),

    path('admin/my_book_header/<int:book_id>', views_admin_book_header.edit_header, name='my_book_header'),
    path('admin/save_header_image/<int:book_id>', views_admin_book_header.save_header_image, name='save_header_image'),

    # ゲームのアップロードに関するURL
    path('admin/game/view', views_admin_game.view, name='game_view'),
    path('admin/game/upload', views_admin_game.upload, name='game_upload'),

    path('admin/access_log', views_admin_access_log.index, name='access_log')
]