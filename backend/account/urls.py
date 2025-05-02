from django.urls import path
from . import views
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

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
    path('password_change/', views.password_change, name='password-change'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html',
                                                                email_template_name='password/password_reset_email.html',
                                                                success_url=reverse_lazy('account:password_reset_done')), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),    
    path('password_reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html',
                                                                                        success_url=reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),

    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
]