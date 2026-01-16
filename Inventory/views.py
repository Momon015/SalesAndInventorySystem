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

from django.core.paginator import Paginator

# Create your views here.

def material_list(request):
    
    form = MaterialFilterForm(request.GET or None)
    materials = Material.objects.all()

    
    total_items = materials.count()
    out_of_stock = materials.filter(quantity__lte=0).count()
    
    """
    this allows to filter things without 
    causing any bugs like not showing anything 
    in template to ensure this always work
    """
    categories = form.fields['category'].queryset 
    
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
        
    # pagination
    paginator = Paginator(materials, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
           

    context = {'page_obj': materials, 'categories': categories, 'out_of_stock': out_of_stock, 'page_obj': page_obj, 'total_items': total_items}
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

def material_detail(request, slug):
    material = get_object_or_404(Material, slug=slug)
    
    context = {'material': material}
    return render(request, 'inventory/material_detail.html', context)

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