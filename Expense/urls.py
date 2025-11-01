from . import views
from django.urls import path

# Create your urls here.

urlpatterns = [
    path('materials/list/', views.material_list, name='material-list'),
    path('materials/create/', views.material_create, name='material-create'),
    path('materials/update/<slug:slug>/', views.material_update, name='material-update'),
    path('materials/delete/<slug:slug>/', views.material_delete, name='material-delete'),
]
