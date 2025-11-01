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

from Expense.models import Material
from Expense.forms import MaterialForm

# Create your views here.

def material_list(request):
    materials = Material.objects.filter()
    
    context = {'materials': materials}
    return render(request, 'Expense/material_list.html', context)

def material_create(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        
        if form.is_valid():
            material = form.save()
            messages.success(request, f"{material.name} successfully created.")
            return redirect('material-list')
        else:
            print('Errors: ', form.errors)
    else:
        form = MaterialForm()
        
    context = {'form': form}
    return render(request, 'Expense/material_create.html', context)

def material_update(request, slug):
    material = get_object_or_404(Material, slug=slug)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        
        if form.is_valid():
            form.save()
            messages.success(request, f"{material.name} successfully updated.")
            
            return redirect('material-list')
        else:
            print('Errors: ', form.errors)
    else:
        form = MaterialForm(instance=material)
        
    context = {'form': form, 'material': material}
    return render(request, 'Expense/material_update.html', context)

def material_delete(request, slug):
    material = get_object_or_404(Material, slug=slug)
    
    if request.method == 'POST':
        material.delete()
        messages.success(request, f"{material.name} successfully deleted.")
        return redirect('material-list')
    
    
    context = {'material': material}
    return render(request, 'Expense/material_delete.html', context)
