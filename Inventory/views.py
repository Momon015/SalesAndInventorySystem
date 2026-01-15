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

from Inventory.models import Material
from Inventory.forms import MaterialForm, MaterialFilterForm

from django.db.models import Q

# Create your views here.

def material_list(request):
    
    """FIX the dropdown issue"""
    form = MaterialFilterForm(request.GET or None)
    materials = Material.objects.all()

    stock_filter = request.GET.get('stock')
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = request.GET.get('category')
        
        if search:
            materials = materials.filter(
                Q(name__icontains=search) |
                    Q(price__icontains=search) |
                    Q(quantity__icontains=search) |
                    Q(category__name__icontains=search)
            )
        if category:
            materials = materials.filter(category=category)
            
        if stock_filter == 'high':
            materials = materials.filter(quantity__gte=50)
            
        elif stock_filter == 'low':
            materials = materials.filter(
                Q(quantity__gte=1) & Q(quantity__lte=25)
            )
        
        elif stock_filter == 'none':
            materials = materials.filter(quantity=0)
    else:
        print('form errors', form.errors)
           

    context = {'materials': materials}
    return render(request, 'Inventory/material_list.html', context)

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
    return render(request, 'Inventory/material_create.html', context)

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
    return render(request, 'Inventory/material_update.html', context)

def material_delete(request, slug):
    material = get_object_or_404(Material, slug=slug)
    
    if request.method == 'POST':
        material.delete()
        messages.success(request, f"{material.name} successfully deleted.")
        return redirect('material-list')
    
    
    context = {'material': material}
    return render(request, 'Inventory/material_delete.html', context)