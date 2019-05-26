from django.contrib import admin
from django.urls import path, include
from dangdangapp import views

app_name = 'dangdangapp'

urlpatterns = [
    path('book_details/',views.book_details,name='book_details'),
    path('book_list/',views.book_list,name='book_list'),
    path('indent/',views.indent,name='indent'),
    path('indent_ok/',views.indent_ok,name='indent_ok'),
    path('index/',views.index,name='index'),
    path('kill_session/',views.kill_session,name='kill_session'),
    path('choose/',views.choose,name='choose'),
    path('present/',views.present,name='present'),

]