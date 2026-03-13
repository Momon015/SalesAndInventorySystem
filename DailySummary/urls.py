from . import views
from django.urls import path

# Create your urls here.

urlpatterns = [
    path('view/list/summary/', views.view_summary, name='view-summary'),
    path('view/list/summary/<str:date>/detail/', views.view_summary_detail, name='view-summary-detail'),
]
