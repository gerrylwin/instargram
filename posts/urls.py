from django.urls import path
from . import views
app_name = 'posts'

urlpatterns = [
    path('', views.list, name="list"),
    path('new/', views.new, name="new"),
    path('<int:post_pk>/', views.detail, name="detail"),
    path('<int:post_pk>/edit/', views.edit, name="edit"),
    path('<int:post_pk>/delete/', views.delete, name="delete"),
    path('<int:post_pk>/new_comment/', views.new_comment, name="new_comment"),
    path('<int:post_pk>/like/', views.like, name="like"),
]