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

from Expense.models import Material, PurchaseItem, Purchase
from Expense.forms import MaterialForm, PurchaseForm, PurchaseItemForm

from decimal import Decimal

# logging
import logging

# Create your views here.

logger = logging.getLogger('Expense')

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

def purchase_list(request):
    purchases = Purchase.objects.filter()
    
    context = {'purchases': purchases}
    return render(request, 'Expense/purchase_list.html', context)

"""clearing cart just in case there's a bug """

def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, "Cart has been reset.")
    return redirect('view-cart')

"""clearing cart just in case there's a bug """

def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    material = get_object_or_404(Material, id=id) 
    material_slug = material.slug
    
    material_key = str(material.id) 
    if material_key in cart:
        if cart[material_key]['quantity'] < material.quantity:
            cart[material_key]['quantity'] += 1

        else:
            messages.warning(request, "You have reached the maximum stock for this item.")
    
    else:
        # first time adding to the cart.
        cart[material_key] = {
            'id': material.id,
            'slug': material_slug,
            'name': material.name,
            'price': float(material.price),
            'quantity': 1,
            'discount': 0,
        }
        messages.success(request, f"{material.name} added to the cart.")

    # LOGGING: add to cart
    logger.debug(f"Current Session Cart: {request.session.get('cart')}")
    
    # save the session
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect('material-list')
    
def view_cart(request):
    cart = request.session.get('cart', {})
    subtotal = 0
    total_discount = 0
    cart_items = []
    
    for material_id, data in cart.items():
        material = get_object_or_404(Material, id=material_id)
        material_slug = material.slug
        discount = data.get('discount', 0)
        quantity = data.get('quantity', 1)
        
        # computations 
        item_total = material.price * quantity
        item_discount = item_total - discount
        total_discount += discount
        subtotal += item_total
        
        cart_items.append({
            'id': material_id,
            'slug': material_slug,
            'material': material.name,
            'quantity': quantity,
            'subtotal': subtotal,
            'price': material.price,
            'item_total': item_total,
            'discount': discount,
            'item_discount': item_discount,
        })
        
        
    total_after_discount = max(subtotal - total_discount, 0)
    
    # LOGGING: View Cart 
    logger.debug(f" View Cart Sessions: {request.session.get('cart')}")
    
    context = {'total_after_discount': total_after_discount, 'cart_items': cart_items, 'subtotal': subtotal, 'total_discount': total_discount}
    return render(request, 'Expense/view_cart.html', context)

def view_cart_summary(request):
    cart = request.session.get('cart', {})
    subtotal = 0
    total_discount = 0
    cart_items = []
    
    for material_id, data in cart.items():
        material = get_object_or_404(Material, id=material_id)
        material_slug = material.slug
        discount = data.get('discount', 0)
        quantity = data['quantity']
        
        # computations 
        item_total = material.price * quantity
        item_discount = item_total - discount
        total_discount += discount
        subtotal += item_total
        
        cart_items.append({
            'name': material.name,
            'slug': material_slug,
            'price': material.price,
            'item_total': item_total,
            'quantity': quantity,
            'discount': discount,
            'item_discount': item_discount,
        })

    total_after_discount = max(subtotal - total_discount, 0)
    
    # LOGGING: View Cart Summary
    logger.debug(f"View Summary Cart Sessions: {request.session.get('cart')}")
    
    context = {'subtotal': subtotal, 'total_after_discount': total_after_discount, 'cart_items': cart_items, 'total_discount': total_discount}
    return render(request, 'Expense/view_cart_summary.html', context)

def confirm_purchase_summary(request):
    cart = request.session.get('cart', {})
    subtotal = 0
    total_discount = 0
    
    purchase = Purchase.objects.create(total_cost=0)
    
    for material_id, data in cart.items():
        material = get_object_or_404(Material, id=material_id)
        discount = data.get('discount', 0)
        quantity = data['quantity']
        
        # computations 
        item_total = material.price * quantity
        total_discount += discount
        subtotal += item_total
        
        if material.quantity < quantity:
            messages.warning(request, f"{material.name} is out of stock.")
            purchase.delete()
             
        # reduce the material's stock 
        material.quantity -= quantity
        material.save()

        item = PurchaseItem.objects.create(
        purchase=purchase,
        material=material,
        discount=data['discount'],
        quantity=data['quantity'],
        )
        
    # check if there's a discount
    total_after_discount = max(subtotal - total_discount, 0)
    
    # save the purchase object
    purchase.total_cost = total_after_discount
    purchase.save()
    
    # save the purchase ID for ref
    request.session['purchase_id'] = purchase.id
    
    # clear the session
    request.session['cart'] = {}
    request.session.modified = True

    return redirect('view-purchase-summary', purchase.id)

def view_purchase_summary(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    purchase_items = purchase.materials.select_related('material')
    
    total_discount = 0
    subtotal = 0
    cart_items = []
    for item in purchase_items:
        item_total = item.material.price * item.quantity
        quantity = item.quantity
        
        # handling discount items
        discount = item.discount
        item_discount = item_total - discount
        total_discount += discount
        
        subtotal += item_total
        
        cart_items.append({
            'name': item.material.name,
            'price': item.material.price,
            'quantity': quantity,
            'item_total': item_total,
            'discount': discount,
            'item_discount': item_discount,

        })

    context = {'cart_items': cart_items, 'subtotal': subtotal, 'total_cost': purchase.total_cost, 'total_discount': total_discount, 'purchase': purchase}
    return render(request, 'Expense/view_purchase_summary.html', context)
    
def cart_remove_materials(request, id):
    cart = request.session.get('cart', {})
    material = get_object_or_404(Material, id=id)
    
    material_key = str(material.id)
    
    if material_key in cart:
        del cart[material_key]
        messages.success(request, f"{material.name} has been removed from the cart.")
         
    request.session.modified = True
    return redirect('view-cart')

def cart_edit_material(request, id):
    cart = request.session.get('cart', {})
    material = get_object_or_404(Material, id=id)

    material_key = str(material.id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            quantity = 1
            
        cart[material_key]['quantity'] = quantity
        messages.success(request, f"{material.name}'s quantity has been updated.")
        request.session.modified = True
    
    return redirect('view-cart')

def cart_discount_material(request):
    cart = request.session.get('cart', {})
    
    for material_id, data in cart.items():

        discount_input = int(request.POST.get(f"discount_{material_id}", 0))
        cart[material_id]['discount'] = discount_input
    

    
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect('view-cart')
        

