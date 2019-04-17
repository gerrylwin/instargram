from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.signup, name = "signup"),
    path('login/', views.login, name = "login"),
    path('logout/', views.logout, name = "logout"),
    path('<int:user_pk>/', views.mypage, name = "mypage"),
    path('delete/', views.delete, name = "delete"),
    path('edit/', views.edit, name = "edit"),
    path('password/', views.password, name='password'),
    path('<int:user_pk>/follow', views.follow, name='follow'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_update, name='profile_update'),
    path('user_list/', views.user_list, name="user_list"),
]
