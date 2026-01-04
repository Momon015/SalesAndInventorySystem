from . import views
from django.urls import path

# Create your urls here.

urlpatterns = [
    path('register-form/', views.register_form, name='register-form'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('profile/<slug:slug>/', views.user_profile, name='user-profile'),
    path('delete/<slug:slug>/', views.user_delete, name='user-delete'),
    
    path('edit/profile/password/', views.user_edit_password, name='user-edit-password'),
    # path('edit/profile/reset/password/', views.user_reset_password, name='user-reset-password'),
    path('edit/profile/<slug:slug>/', views.user_edit_profile, name='user-edit-profile'),

]
