from django.shortcuts import render, redirect
from django.http import HttpResponse
# ログイン機能
from django.contrib.auth import authenticate, login
from django.contrib import messages
# application/write_data.pyをインポートする
from .application import write_data
# 以下モデル
from .models import User
# Create your views here.
def Login(request):
    params = {
        'title' : 'ログイン画面',
        'data' : [],
    }
    
    if (request.method == 'POST'):
        # この２つはhtml上に記入された文字列
        # このget内の引数もUserクラスの変数名と同じにしないといけない
        username = request.POST.get('userName')
        password = request.POST.get('password')

        # ユーザー名がデータベースにない場合の例外処理
        try:
            # ログイン画面で入力したユーザー名の情報(Userクラスの変数)を取得
            item = User.objects.get(userName=username)
            if (item.userName == username):
                if (item.password == password):
                    if (item.masterMode):
                        return redirect('ReserveApp:ManagerMainMenu')
                    else:
                        return redirect('ReserveApp:UserMainMenu')
                else:
                    messages.error(request, 'パスワードが間違っています。')
                    # return redirect('ManagementApp:UserEntry')
            else:
                messages.error(request, 'ユーザー名が間違っています。')
        except:
            messages.error(request, 'ユーザー名を入力してください。')
            # return redirect('ManagementApp:Login')
    return render(request, 'login.html', params)

def Logout(request):
    return render(request, 'logout.html')



def ManagerMainMenu(request):
    params = {
        'title' : 'メインメニュー（管理者）',
        'message' : ''
    }
    return render(request, 'ManagerMainMenu.html', params)

def UserMainMenu(request):
    params = {
        'title' : 'メインメニュー',
        'message' : ''
    }
    return render(request, 'UserMainMenu.html', params)


# ajaxでurl指定したメソッド
def call_write_data(req):
    if req.method == 'GET':
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        write_data.write_csv(req.GET.get("input_data"))
        return HttpResponse()