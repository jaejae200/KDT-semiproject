from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.core.paginator import Paginator

# Create your views here.

# 로그인
def signup(request):
    if request.method == 'POST':
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        signup_form = CustomUserCreationForm()

    context = {
        'signup_form' : signup_form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        login_form = AuthenticationForm()

    context = {
        'login_form' : login_form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    messages.warning(request, '로그아웃 하였습니다.')
    return redirect('articles:index')

def detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)

    context = {
        'user': user,
    }
    return render(request, 'accounts/detail.html', context)
    
@login_required
def update(request):
    if request.method == 'POST':
        update_form = CustomUserChangeForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('accounts:detail', request.user.pk)
    else:
        update_form = CustomUserChangeForm(instance=request.user)
    context = {
        'update_form': update_form
    }
    return render(request, 'accounts/update.html', context)

@login_required
def follow(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.user == user:
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('accounts:detail', pk)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return redirect('accounts:detail', pk)
