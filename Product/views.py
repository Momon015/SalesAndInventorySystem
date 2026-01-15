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
from Product.models import Product
from Product.forms import ProductForm, ProductFilterForm

from django.db.models import Q
# Create your views here.

def product_list(request):
    form = ProductFilterForm(request.GET or None)
    products = Product.objects.all().order_by('created_at')
    
    """
    this allows to filter things without 
    causing any bugs like not showing anything 
    in template to ensure this always work
    """
    categories = form.fields['category'].queryset
    
    print('form errors', form.errors)
    print('form valid', form.is_valid())
    
    

    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        
        if search:

            products = products.filter(
                Q(name__icontains=search) | 
                Q(category__name__icontains=search) | 
                Q(description__icontains=search) |
                Q(category__category_type__icontains=search) 
                
            )
        if category:
            products = products.filter(category=category)
    
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj, 'paginator': paginator, 'form': form, 'categories': categories}
    return render(request, 'Product/product_list.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.description = product.description.title()
            product.name = product.name.title()
            product.save()

            messages.success(request, f"{product.name} has been created.")
            return redirect('product-list')
        else:
            print('Errors: ', form.errors)
    
    else:
        form = ProductForm()
        
    context = {'form': form}
    return render(request, 'Product/product_create.html', context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    context = {'product': product}
    return render(request, 'Product/product_detail.html', context)


def product_update(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
  
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.name = product.name.lower()
            product.save()
            messages.success(request, f"{product.name} has been updated.")
            return redirect('product-detail', product.slug)
        else:
            print('Errors: ', form.errors)
    else:
        form = ProductForm(instance=product)
        
    context = {'form': form, 'product': product}
    return render(request, 'Product/product_update.html', context)


def product_delete(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"{product.name} has been deleted.")
        return redirect('product-list')
    
    context = {'product': product}
    return render(request, 'Product/product_delete.html', context)
        
        