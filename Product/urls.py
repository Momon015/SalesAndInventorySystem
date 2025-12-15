from . import views
from django.urls import path

# Create your urls here.

urlpatterns = [
    path('list/', views.product_list, name='product-list'),
    path('create/', views.product_create, name='product-create'),
    path('detail/<slug:product_slug>/', views.product_detail, name='product-detail'),
    path('update/<slug:product_slug>/', views.product_update, name='product-update'),
    path('delete/<slug:product_slug>/', views.product_delete, name='product-delete'),
]


