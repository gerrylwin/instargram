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
]
