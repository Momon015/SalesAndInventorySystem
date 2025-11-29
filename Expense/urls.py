from . import views
from django.urls import path

# Create your urls here.

urlpatterns = [
    # materials urls
    path('materials-list/', views.material_list, name='material-list'),
    path('materials/create/', views.material_create, name='material-create'),
    path('materials/update/<slug:slug>/', views.material_update, name='material-update'),
    path('materials/delete/<slug:slug>/', views.material_delete, name='material-delete'),
    
    # purchase urls
    path('purchase/materials-list/', views.purchase_list, name='purchase-list'),
    
    # cart sessions
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add-cart'),
    path('view-cart/', views.view_cart, name='view-cart'),
    path('view/checkout-summary/', views.view_cart_summary, name='view-checkout-summary'),
    path('view/confirm/purchase-summary/', views.confirm_purchase_summary, name='purchase-summary'),
    path('view/purchase-summary/<int:purchase_id>/', views.view_purchase_summary, name='view-purchase-summary'),

    
    # edit material's quantity from session
    path('edit/<int:id>/', views.cart_edit_material, name='cart-edit-material'),
    
    # delete material from session
    path('delete/<int:id>/', views.cart_remove_materials, name='cart-remove-material'),
    
    # edit material's price from session
    path('', views.cart_discount_material, name='cart-discount-material'),

    # clear cart sessions
    path('cart/clear/', views.clear_cart, name='clear-cart'),
]
