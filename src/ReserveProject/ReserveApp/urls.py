from django.urls import path
from . import views

app_name = 'ReserveApp'
urlpatterns = [path('login/', views.Login,  name="Login"),
                path('logout/', views.Logout, name="Logout"),
                path("ajax/", views.call_write_data, name="call_write_data"),
                path('managermainmenu/', views.ManagerMainMenu, name='ManagerMainMenu'),
                path('usermainmenu/', views.UserMainMenu, name="UserMainMenu"),
                path('userDB/', views.UserDB, name="UserDB"),
                path('edit/<int:num>', views.UserEdit, name="Edit"),
                path('delete/<int:num>', views.UserDelete, name="Delete"),
                path('reserveMenu/', views.ReserveMenu, name="ReserveMenu"),
                path('calendar/', views.week_calendar, name='week_calendar'),
                path('calendar/<int:year>/<int:month>/<int:day>/', views.week_calendar, name='week_calendar_specific'),
                path('EntryTime/', views.EntryTime, name="EntryTime"),
                path('MyReserve/', views.MyReserve, name="MyReserve")]