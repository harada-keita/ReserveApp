from django.shortcuts import render, redirect
from django.http import HttpResponse
# ログイン機能
from django.contrib import messages
# application/write_data.pyをインポートする
from .application import write_data
# 以下モデル
from .models import User, Schedule, Place
from .forms import UserDBForm, UserForm, UserCreateForm
#以下カレンダー

import datetime


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
            userID = item.id
            if (item.userName == username):
                if (item.password == password):
                    if (item.masterMode):
                        # ユーザー名を他のページで使用するため
                        request.session['username'] = username
                        #予約マイページを表示するため、Userのidを取得できるようにする（ユーザー名ではモデル情報を取得できなかった）
                        request.session['userID'] = userID
                        return redirect('ReserveApp:ManagerMainMenu')
                    else:
                        # ユーザー名を他のページで使用するため
                        request.session['username'] = username
                        #予約マイページを表示するため、Userのidを取得できるようにする（ユーザー名ではモデル情報を取得できなかった）
                        request.session['userID'] = userID
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
        name = request.POST['userName']
        # get内の引数の「userName」の所はUserクラスの変数名じゃないとだめ
        item = User.objects.get(userName=name)
        params['data'] = [item]
        params['form'] = UserForm(request.POST)
    else:
        params['data'] = User.objects.all()
    return render(request, 'UserDB.html', params)

def UserCreate(request):
    params = {
        'title' : 'ユーザー登録',
        'message' : 'your data:',
        'form' : UserCreateForm()
    }
    if (request.method == 'POST'):
        params['title'] = '登録しました。'
        obj = User()
        user = UserCreateForm(request.POST, instance=obj)
        user.save()
    return render(request, 'UserCreate.html', params)
    


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
    

    
def week_calendar(request, year=None, month=None, day=None):
    place = '会議室１'
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
    #print(reserved_data)
    for index, date in enumerate(dates):#こっち(date)は表示する日付
        #print(date.date())
        for i in reserved_data:#こっち(i)が予約されているデータ
            #print(i.start.date())
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
        print(date)
        date_str = date.split(" ")[0] #datetime型に変換するために文字列内から必要な文字のみを取得
        time = request.session.get("time")
        start_time = time.split("～")[0] # 9:00～10:00の場合、9:00の部分を取得
        print(date)
        combine_datetime = date_str + " " + start_time #年月日 時:分
        
        reserve_start_datetime = datetime.datetime.strptime(combine_datetime, "%Y-%m-%d %H:%M")
        reserve_end_datetime = reserve_start_datetime + datetime.timedelta(hours=1)
        #ユーザーモデルを取得するためのユーザー名のstrを取得
        user_name = request.session.get('username')
        #ユーザーモデル情報を取得
        reserve_user = User.objects.get(userName=user_name)
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
    username = request.session.get('username')
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
    username = request.session.get('username')
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