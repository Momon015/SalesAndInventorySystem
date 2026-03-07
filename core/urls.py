from . import views
from django.urls import path


# Create your urls here.

urlpatterns = [
    path('category-list/', views.category_list, name='category-list'),
    path('category/create/', views.category_create, name='category-create'),
    path('category/update/<int:category_id>/', views.category_update, name='category-update'),
    path('category/delete/<int:category_id>/', views.category_delete, name='category-delete'),
]
