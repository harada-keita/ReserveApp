from django.shortcuts import render, redirect
from django.http import HttpResponse
# ログイン機能
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# application/write_data.pyをインポートする
from .application import write_data
# 以下モデル
from .models import User, Schedule, Place
from .forms import UserDBForm, UserForm
#以下カレンダー
import datetime
from zoneinfo import ZoneInfo
from django.utils.timezone import make_aware
import pytz



# Create your views here.
def Login(request):
    params = {
        'title' : 'ログイン画面'
    }
    if request.method == 'POST':
        input_username = request.POST.get('username')
        input_password = request.POST.get('password')
        print(input_username)
        print(input_password)
        user = authenticate(request=request, username=input_username, password=input_password)
        if user is not None:
            # 以下他のページでユーザー名などの情報を使用するためにデータ確保
            user = User.objects.get(username=input_username)
            request.session['user_name'] = user.username
            # request.session['is_staff'] = user.is_staff
            # request.session['is_superuser'] = user.is_superuser
            login(request, user)
            return redirect('ReserveApp:MyPage_Admini')  # ログイン後の遷移先
        else:
            messages.error(request, 'ユーザー名またはパスワードが間違っています')
    return render(request, 'login.html', params)


def Logout(request):
    logout(request)
    return render(request, 'logout.html')

@login_required
def MyPage_Admini(request):
    # ログインページからユーザー名を取得
    username = request.session.get('user_name')
    mode_str = None
    # ユーザー名からモデル情報を取得
    user = User.objects.get(username=username)
    if user.is_staff:
        mode_str = "（管理者）"
    mail = user.email
    params = {
        'username' : f"{username}{mode_str}",
        'mail' : f"メールアドレス : {mail}"
    }
    return render(request, 'MyPage_Admini.html', params)

def ManagerMainMenu(request):
    #ログインページからユーザー名を取得
    username = request.session.get('username')

    # if request.method == "POST":
    #     selected_value = request.POST.get("example")
    params = {
        'title' : 'メインメニュー（管理者）',
        'message' : f'{username}さんのページ',
        'ButtonMessage': '予約画面へ'
        
    }
    
    return render(request, 'ManagerMainMenu.html', params)

def UserMainMenu(request):
    params = {
        'title' : 'メインメニュー',
        'message' : ''
    }
    return render(request, 'UserMainMenu.html', params)

def ReserveMenu(request):
    params = {
        'title' : '予約システム'
    }
    return render(request, 'ReserveMenu.html', params)

def UserDB(request):
    params = {
        'title' : 'ユーザー情報',
        'message' : 'all Persons',
        'form' : UserDBForm(),
        'data' : []
    }
    if (request.method == 'POST'):
        name = request.POST['username']
        # get内の引数の「userName」の所はUserクラスの変数名じゃないとだめ
        item = User.objects.get(username=name)
        params['data'] = [item]
        params['form'] = UserForm(request.POST)
    else:
        params['data'] = User.objects.all()
    return render(request, 'UserDB.html', params)


def UserCreate(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ユーザー登録が完了しました')
            return redirect('ReserveApp:Login')  # 登録後ログイン画面へ
        else:
            messages.error(request, '入力内容に誤りがあります')
    else:
        form = UserForm()
    return render(request, 'UserCreate.html', {'title': 'ユーザー登録', 'form' : form})


def UserEdit(request, num):
    obj = User.objects.get(id=num)
    if (request.method == 'POST'):
        user = UserForm(request.POST, instance=obj)
        user.save()
        return redirect('ReserveApp:UserDB')
    params={
        'title' : 'ユーザー編集画面',
        'id' : num,
        'form' : UserForm(instance=obj)#ここの書き方はforms.pyで定義したFormがModelFormを継承した場合に使用可能。
    }
    return render(request, 'UserEdit.html', params)

def UserDelete(request, num):
    user = User.objects.get(id=num)
    if (request.method == 'POST'):
        user.delete()
        return redirect('ReserveApp:UserDB')
    params={
        'title' : 'ユーザー削除',
        'id' : num,
        'obj' : user,
    }
    return render(request, 'UserDelete.html', params)

# ajaxでurl指定したメソッド
def call_write_data(req):
    if req.method == 'GET':
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        write_data.write_csv(req.GET.get("input_data"))
        return HttpResponse()
    

@login_required
def week_calendar(request, year=None, month=None, day=None):
    place = '会議室A'
    nine_time_result = []
    ten_time_result = []
    eleven_time_result = []
    twelve_time_result = []
    thirteen_time_result = []
    fourteen_time_result = []
    fifteen_time_result = []
    sixteen_time_result = []
    seventeen_time_result = []
    
    #とりあえず表内を〇で埋める処理をしてから、条件分岐で×に変換
    for i in range(7):
        previous = '〇'
        nine_time_result.append(previous)
        ten_time_result.append(previous)
        eleven_time_result.append(previous)
        twelve_time_result.append(previous)
        thirteen_time_result.append(previous)
        fourteen_time_result.append(previous)
        fifteen_time_result.append(previous)
        sixteen_time_result.append(previous)
        seventeen_time_result.append(previous)
    
    #表の日付のstr
    if year and month and day:
        date_str = f"{year}年{month}月{day}日"
        today = datetime.datetime.strptime(date_str, "%Y年%m月%d日")
    else:
        today = datetime.datetime.now()
    #次週、前週の場合の切り替え
    start_week = today - datetime.timedelta(days=today.weekday())
    dates = [start_week + datetime.timedelta(days=i) for i in range(7)]
    next_week = start_week + datetime.timedelta(days=7)
    prev_week = start_week - datetime.timedelta(days=7)

    reserved_data = []
    reserved_data = Schedule.objects.all()
    print(reserved_data)
    for index, date in enumerate(dates):#こっち(date)は表示する日付
        print(date.date())
        for i in reserved_data:#こっち(i)が予約されているデータ
            print(i.start.date())
            #日付が一致した場合
            if i.start.date() == date.date():
                print(i.start.hour)
                #予約のスタート時間が9の場合9:00～10:00を×
                if i.start.hour == 9:
                    nine_time_result[index] = '×'
                elif i.start.hour == 10:
                    ten_time_result[index] = '×'
                elif i.start.hour == 11:
                    eleven_time_result[index] = '×'
                elif i.start.hour == 12:
                    twelve_time_result[index] = '×'
                elif i.start.hour == 13:
                    thirteen_time_result[index] = '×'
                elif i.start.hour == 14:
                    fourteen_time_result[index] = '×'
                elif i.start.hour == 15:
                    fifteen_time_result[index] = '×'
                elif i.start.hour == 16:
                    sixteen_time_result[index] = '×'
                elif i.start.hour == 17:
                    seventeen_time_result[index] = '×'

    
    context = {
        'title' : "予約画面",
        'message' : place,
        'dates': dates,
        'today': today,
        'next_week_year': next_week.year,
        'next_week_month': next_week.month,
        'next_week_day': next_week.day,
        'prev_week_year': prev_week.year,
        'prev_week_month': prev_week.month,
        'prev_week_day': prev_week.day,
        '9time' : nine_time_result,
        '10time' : ten_time_result,
        '11time' : eleven_time_result,
        '12time' : twelve_time_result,
        '13time' : thirteen_time_result,
        '14time' : fourteen_time_result,
        '15time' : fifteen_time_result,
        '16time' : sixteen_time_result,
        '17time' : seventeen_time_result

    }
    return render(request, 'calendar.html', context)

def ReserveDisplay(request):

    if (request.method == 'POST'):
        date = request.session.get("day")
        date_str = date.split(" ")[0] #datetime型に変換するために文字列内から必要な文字のみを取得
        time = request.session.get("time")
        start_time = time.split("～")[0] # 9:00～10:00の場合、9:00の部分を取得
        combine_datetime_str = date_str + " " + start_time #年月日 時:分
        # 下のlocalizeの引数はdatetime型の必要があるためstrから変換
        combine_datetime = datetime.datetime.strptime(combine_datetime_str, "%Y-%m-%d %H:%M")
        # UTCとして扱いたい場合（タイムゾーンの影響を受けない）←「setting.py」のタイムゾーンを東京にした状態で表の時間を取得すると自動で変換されて異なる時間が予約されたことになってしまう
        dt_utc = pytz.utc.localize(combine_datetime)
        # 予約の開始時間（表と同じ日時）
        reserve_start_datetime = dt_utc
        # 予約の終了時間（開始時間＋１時間）
        reserve_end_datetime = reserve_start_datetime + datetime.timedelta(hours=1)
        #ユーザーモデルを取得するためのユーザー名のstrを取得(マイページから？)
        user_name = request.session.get('user_name')
        #ユーザーモデル情報を取得
        reserve_user = User.objects.get(username=user_name)
        #場所はとりあえずベタ打ちで登録(ユーザーと同様)
        place_name = '会議室A'
        reserve_place = Place.objects.get(name=place_name)
        Schedule.objects.create(user=reserve_user, place=reserve_place, start=reserve_start_datetime, end=reserve_end_datetime)
        return redirect('ReserveApp:week_calendar')
    
    time = request.GET.get("time")
    #本ページ内でボタンを押すと上記（2回目）ではデータはNONEになってします⇒request.sessionで保管する
    request.session['time'] = time
    date = request.GET.get("day")
    request.session['day'] = date
    params = {
        'title': '予約画面',
        'message' : '以下の時間帯で予約しますか',
        'date' : date,
        'time' : time
    }
    return render(request, 'ReserveDisplay.html', params)



def MyReserve(request):
    # ログインページからユーザー名を取得
    username = request.session.get('user_name')
    #ユーザー情報を取得するためにIDを取得
    userID = request.session.get('userID')
    params = {
        'title' : f"{username}さんの予約状況",
        'data' : []
    }

    #ログインしたユーザーの予約情報を取得(以下のgetは一件だけ取得できるらしい←同一ユーザーの登録が２件以上ある場合エラー発生⇒getではなくfilter)
    item = Schedule.objects.filter(user=userID).order_by('start')
    params['data'] = item#ここのitemに配列の[]をつけてしまうと二次元配列（余計な次元となってしまうため、なしで）

    return render(request, 'MyReserve.html', params)

def ReserveDelete(request, num):
    username = request.session.get('user_name')
    user = User.objects.get(userName=username)
    schedule = Schedule.objects.get(id=num, user=user)
    if (request.method == 'POST'):
        schedule.delete()
        return redirect('ReserveApp:MyReserve')
    params = {
        'title' : 'この時間の予約を削除しますか',
        'obj' : schedule
    }
    return render(request, 'ReserveDelete.html', params)




def PriceList(request):
    return render(request, 'PriceList.html')

def Access(request):
    return render(request, 'Access.html')