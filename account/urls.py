from django.urls import path
from . import views
from django.shortcuts import render

app_name='account'

urlpatterns = [
    #Registration and verification 
    path('register/', views.register_user, name='register'),
    path('email-verification/', lambda request: render(request, 'account/email-verification.html'),
        name='email-verification'
        ),
    
    #login & logout
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),

    #Dashboard
    path('dashboard/', views.dashboard_user, name='dashboard'),
    path('profile-management/', views.profile, name='profile'),
    path('account-delete/', views.delete_user, name='delete-user'),

    #Password change
    path('password_change/', views.password_change, name='password-change')
]