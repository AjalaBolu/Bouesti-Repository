from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_journals, name='search_journals'),
    path('upload/', views.upload_journal, name='upload_journal'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve/<int:journal_id>/', views.approve_journal, name='approve_journal'),
    path('reject/<int:journal_id>/', views.reject_journal, name='reject_journal'),
    path('pending/', views.pending_journals, name='pending_journals'),
    path('approved/', views.approved_journals, name='approved_journals'),
    path('rejected/', views.rejected_journals, name='rejected_journals'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('my-journals/', views.my_journals, name='my_journals'),
]
