from . import views
from django.urls import path

# Create your urls here.

urlpatterns = [
    # purchase urls
    path('view/purchase-history/', views.purchase_history, name='purchase-list'),
    path('view/<int:purchase_id>/purchase-history/', views.purchase_detail, name='purchase-detail'),
    
    # cart sessions
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add-cart'),
    path('view-cart/', views.view_cart, name='view-cart'),
    path('view/checkout-summary/', views.view_cart_summary, name='view-checkout-summary'),
    path('view/confirm/purchase-summary/', views.confirm_purchase_summary, name='purchase-summary'),
    path('view/purchase-summary/<int:purchase_id>/', views.view_purchase_summary, name='view-purchase-summary'),

    # save items
    path('view-cart/save/preset/', views.save_items, name='save-items'),
    path('view/presets/', views.preset_list, name='preset-list'),
    path('view/<int:preset_id>/preset/', views.preset_detail, name='preset-detail'),
    path('edit/<int:preset_id>/preset/', views.edit_preset, name='edit-preset'),
    path('view/preset/<int:preset_id>/delete/', views.delete_preset, name='delete-preset'),
    
    # adding preset to cart
    path('view/<int:preset_id>/apply-preset/', views.adding_preset_to_cart, name='add-preset-to-cart'),
    
    
    # edit material's quantity from session
    path('edit/<int:id>/', views.cart_edit_material, name='cart-edit-material'),
    
    # delete material from session
    path('delete/<int:id>/', views.cart_remove_materials, name='cart-remove-material'),
    
    # edit material's price from session
    path('', views.cart_discount_material, name='cart-discount-material'),

    # clear cart sessions
    path('view/cart/clear/', views.clear_cart, name='clear-cart'),
]
