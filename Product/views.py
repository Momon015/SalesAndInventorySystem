from django.shortcuts import render

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

from Product.models import Product
from Product.forms import ProductForm

# Create your views here.

def product_list(request):
    products = Product.objects.filter()
    
    context = {'products': products}
    return render(request, 'Product/product_list.html', context)

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Product successfully created.")
            return redirect('product-list')
        else:
            print('Errors: ', form.errors)
    else:
        form = ProductForm()
        
    context = {'form': form, 'success': "Product successfully created."}
    return render(request, 'Product/product_create.html', context)

def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Product successfully updated.")
            return redirect('product-list')
        else:
            print('Errors: ', form.errors)
    else:
        form = ProductForm(instance=product)
        
    context = {'form': form, 'success': "Product successfully updated."}
    return render(request, 'Product/product_update.html', context)

def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product successfully deleted.")
        return redirect('product-list')
    
    
    context = {'product': product, 'success': "Product successfully deleted."}
    return render(request, 'Product/product_delete.html', context)