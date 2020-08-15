from django.contrib import admin
from django.urls import path
from todoapp import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #auth
    path('account/login/', views.login_view, name= 'login'),
    path('account/logout/', views.logout_user, name='logout'),
    path('account/register/', views.register_view, name='register'),

    #----
    path('admin/', admin.site.urls),
    path('', views.main, name='Main'),
    path('view/<int:id>', views.viewtask, name='Show'),
    path('adding/', views.add, name='Add'),
    path('addit/', views.addit, name='AddIt'),
    path('editing/<int:itemid>', views.edit, name='Edit'),
    path('editit/<int:itemid>', views.editit, name='EditIt'),
    path('removeit/<int:itemid>', views.removeit, name='RemoveIt'),
    path('clearall/', views.clearall, name='Clear'),
    path('changed/<int:itemid>/<str:change>>', views.changed, name='Change'),
    # path('main2/', views.main2, name='new_main'),
    # path('main3/', views.home3, name='newer_main'),
    #api
    path('api_show/', views.api_show, name='API_Show'),
    path('api_update/', views.api_update, name='API_Update'),
    path('api_del/', views.api_del, name='API_Del'),
    path('api_add/', views.api_add, name='API_Add'),
    path('api/register/', views.api_register, name='API_Register'),
    path('api/login/', obtain_auth_token, name='API_Login'),
    #---
]
