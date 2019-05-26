from django.urls import path, include
from carapp import views

app_name = 'carapp'

urlpatterns = [
    path('car/',views.car,name='car'),
    path('add_book/',views.add_book,name='add_book'),
    path('change_num/',views.change_num,name='change_num'),
    path('del_num/',views.del_num,name='del_num'),
    path('update_book/',views.update_book,name='update_book'),
    path('recover/',views.recover,name='recover'),

]