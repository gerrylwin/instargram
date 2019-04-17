from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, UserEditForm, ProfileForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from .models import Profile

# Create your views here.
def signup(request):
    if request.method=="POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            Profile.objects.create(user=user)
            auth_login=(request, user)
            messages.info(request, f'{user.username}님, 회원가입 성공!')
            return redirect('posts:list')
        messages.warning(request, '양식을 다시 확인해주세요.')
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
            if request.user.profile.nickname:
                return redirect('posts:list')
            return redirect(request.GET.get('next') or 'accounts:profile_update')
    else:    
        login_form = AuthenticationForm()
    context = {'login_form':login_form}
    return render(request, 'login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('posts:list')



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

@login_required
def password(request):
    if request.method == 'POST':
        user_form = PasswordChangeForm(request.user, request.POST) # 순서 주의!
        if user_form.is_valid():
            user = user_form.save()
            update_session_auth_hash(request, user)
            return redirect('posts:list')
    else:
        user_form = PasswordChangeForm(request.user) # instance= 아님 주의!
    context = {'user_form': user_form}
    return render(request, 'edit.html', context)

def profile_update(request):
    if request.method == "POST":
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
            )
        if profile_form.is_valid():
            profile_form.save()
            return redirect('posts:list')
    profile_form = ProfileForm(instance=request.user.profile)
    context = {'profile_form': profile_form}
    return render(request, 'profile_update.html', context)

def profile(request):
    return render(request, 'profile.html')
    
def mypage(request, user_pk):
    user_detail = get_object_or_404(get_user_model(), pk = user_pk)
    context = {'user_detail':user_detail}
    return render(request, 'mypage.html', context)    
    
def follow(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    
    return redirect('accounts:mypage', user_pk)
    
def user_list(request):
    user_list = get_user_model().objects.all()
    context = {'user_list':user_list}
    return render(request, 'user_list.html', context)