from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, FormView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.utils import timezone
from datetime import timedelta
import random

from django.views.decorators.http import require_POST
from django.urls import reverse

from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash

from django.core.paginator import Paginator

from core.models import Category

from user.models import User
from user.forms import RegisterForm, UpdateUserForm, StyledPasswordChangeForm

# Create your views here.

def register_form(request):
    page = 'register-form'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            
            user.username = user.username.lower()
            user.first_name = user.first_name.title()
            user.last_name = user.last_name.title()
            raw_password = form.cleaned_data.get('password1')
            user.set_password(raw_password)
            user.save()
            login(request, user)
            return redirect('product-list')
        else:
            print('form errors:', form.errors)
    else:
        form = RegisterForm()

    context = {'form': form, 'page': page}
    return render(request, 'user/register_and_login_form.html', context)

def user_login(request):
    user = None
    page = 'login'
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            user_obj = None
            messages.error(request, f"Username OR Password is incorrect. Please try again.")
            print('user_obj', user_obj)
            
        if user_obj and user_obj.locked_until and timezone.now() > user_obj.locked_until: # checks if the user is not locked anymore to reset the attempts
            user_obj.reset_attempts()
            user_obj.save()    
            
        if user_obj and user_obj.is_locked(): # checks if user exists and checks if account is locked
            messages.error(request, f"Your account is temporarily locked for 10 mins. Please try again later.")
        else:
            user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            user_obj.reset_attempts()
            user_obj.last_login = timezone.now()
            user_obj.save(update_fields=['last_login'])
            return redirect('product-list')
        else:
            if user_obj and not user_obj.is_locked(): # checks if user exists and the user is not locked
                user_obj.register_failed_login()
                print('Total Attempts:',user_obj.failed_attempts)
                user_obj.save()
                messages.error(request, f"Username OR Password is incorrect. Please try again.")

            return redirect('login')
            
    context = {'page': page}
    return render(request, 'user/register_and_login_form.html', context)
    
def user_profile(request, slug):
    user = get_object_or_404(User, slug=slug)
    
    
    context = {'user': user}
    return render(request, 'user/user_profile.html', context)

def user_edit_profile(request, slug):
    user = get_object_or_404(User, slug=slug)
    
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.name = user.name.title()
            user.first_name = user.first_name.title()
            user.last_name = user.last_name.title()
            user.save()
            messages.success(request, f"Your profile has been updated.")
            return redirect('user-profile', slug=slug)
        
        else:
            print('form errors: ', form.errors)
            
    else:
        form = UpdateUserForm(instance=user)
    
    context = {'form': form, 'page': 'user-edit-profile'}
    return render(request, 'user/edit_user_profile_form.html', context)

def user_edit_password(request):
    if request.method == 'POST':
        form = StyledPasswordChangeForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            user = form.save()
            user.password_changed_at = timezone.now()
            user.save(update_fields=['password_changed_at'])
            update_session_auth_hash(request, user) # keeps the user logged in
            messages.success(request, f"Your Password has succesfully updated.")
            return redirect('user-profile', request.user.slug)
        else:
            print('form errors:', form.errors)
        
    else:
        form = StyledPasswordChangeForm(user=request.user)
    
    context = {'form': form, 'page': 'user-edit-password'}
    return render(request, 'user/edit_user_profile_form.html', context)

# def user_reset_password(request):
#     if request.method == 'POST':
#         form = PasswordResetForm()
        
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, f"Password has succesfully reset.")
#             return redirect('user-profile', user.request.slug)
    
#     else:
#         form = PasswordResetForm()
        
#     context = {'form': form, 'page': 'user-reset-password'}
#     return render(request, 'user/edit_user_profile_form.html', context)

def user_delete(request, slug):
    user = get_object_or_404(User, slug=slug)
    
    if request.method == 'POST':
        user.delete()
        return redirect('product-list')

    context = {'user': user}
    return render(request, 'user/user_delete.html', context)
    
def user_logout(request):
    logout(request)
    return redirect('product-list')