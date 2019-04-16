from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, UserEditForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
# from django.contrib import messages
from django.contrib.auth import get_user_model

# Create your views here.
def signup(request):
    if request.method=="POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('posts:list')
    else:
        user_form = UserForm()
    context = {'user_form':user_form}
    return render(request, 'signup.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == "POST":                                # model에 직접 저장하는게 아닌
        login_form = AuthenticationForm(request, request.POST) # session에 값을 넘겨준다는 느낌
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(request.GET.get('next') or 'posts:list')
    else:    
        login_form = AuthenticationForm()
    context = {'login_form':login_form}
    return render(request, 'login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('posts:list')

def mypage(request, user_pk):
    user_detail = get_object_or_404(get_user_model(), pk = user_pk)
    context = {'user_detail':user_detail}
    return render(request, 'mypage.html', context)

@require_http_methods(["GET", "POST"])
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('accounts:mypage', request.user.pk)
    else:
        user_form = UserEditForm(instance=request.user)
    context = {'user_form':user_form}
    return render(request, 'edit.html', context)

@login_required
def delete(request):
    if request.method == "POST":
        request.user.delete()
    return redirect('posts:list')
        