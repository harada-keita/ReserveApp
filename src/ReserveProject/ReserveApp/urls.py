from django.urls import path
from . import views

app_name = 'ReserveApp'
urlpatterns = [path('login/', views.Login,  name="Login"),
                path('logout/', views.Logout, name="Logout"),
                path("ajax/", views.call_write_data, name="call_write_data"),
                path('managermainmenu/', views.ManagerMainMenu, name='ManagerMainMenu'),
                path('usermainmenu/', views.UserMainMenu, name="UserMainMenu")]