from django.urls import path, include
from log_regist_app import views

app_name = 'log_regist_app'

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('register_ok/',views.register_ok,name='register_ok'),
    path('register_logic/',views.register_logic,name='register_logic'),
    path('login_logic/',views.login_logic,name='login_logic'),
    path('check_username/',views.check_username,name='check_username'),
    path('checkpwd/',views.checkpwd,name='checkpwd'),
    path('checkrepwd/',views.checkrepwd,name='checkrepwd'),
    path('getcaptcha/',views.getcaptcha,name='getcaptcha'),
    path('log_name/',views.log_name,name='log_name'),
    path('log_pwd/',views.log_pwd,name='log_pwd'),
    path('return_where/',views.return_where,name='return_where'),
    path('sendEmail_check/',views.sendEmail_check,name='sendEmail_check'),

]