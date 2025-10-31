from . import views
from django.urls import path

# Create your urls here.

urlpatterns = [
    path('list/', views.product_list, name='product-list'),
    path('create/', views.product_create, name='product-create'),
    path('update/<slug:slug>/', views.product_update, name='product-update'),
    path('delete/<slug:slug>/', views.product_delete, name='product-delete'),
]


