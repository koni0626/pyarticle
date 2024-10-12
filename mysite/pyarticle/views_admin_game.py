import os
import glob
import shutil
import zipfile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .forms import AttachFileForm
from .utils import custom_render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required(login_url='login/')
def view(request):
    """
    添付されたティラノビルダーのフォルダ一覧を表示する
    :param request:
    :return:
    """
    user_id = request.user.id  # ログインしているユーザーのIDを取得

    game_dir_list = [os.path.basename(name) for name in glob.glob(settings.MEDIA_ROOT + f"/game/{user_id}/*")]
    base_url = request.build_absolute_uri('/').rstrip('/')
    data = {"game_dir_list": game_dir_list,
            "user_id": user_id,
            "base_url": base_url,
            "attach_file_form": AttachFileForm()}

    return custom_render(request, 'pyarticle/admin/game/view.html', data)


@login_required(login_url='login/')
def upload(request):
    """
    ティラノビルダーのファイルをzip形式でアップロードする。
    アップロード先のディレクトリはmedia/game/ユーザーID。
    :param request:
    :return:
    """
    if request.method == 'POST' and request.FILES['attach_file']:
        # ログインユーザーのidを取得する
        user_id = request.user.id
        # ユーザーディレクトリ名
        save_dir = settings.MEDIA_ROOT + f"/game/{user_id}"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # ファイルを保存する
        attach_file = request.FILES['attach_file']
        # zipファイルのみ許可する
        file_name, file_ext = os.path.splitext(attach_file.name)
        if file_ext != ".zip":
            raise Http404("アップロードできるファイルはzip形式のみです")

        dst_dir = os.path.join(save_dir, file_name)
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)

        fileobject = FileSystemStorage()
        zip_file_path = os.path.join(save_dir, attach_file.name)
        fileobject.save(zip_file_path, attach_file)
        # ZIPファイルを解凍
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(save_dir)
        # zipファイルを削除する
        os.remove(zip_file_path)

    return redirect('game_view')


@login_required(login_url='login/')
def delete(request):
    """
    ティラノビルダーのファイルを削除する
    :param request:
    :return:
    """


