from django.urls import path
from django.contrib.auth import views as auth_views
from django.template.loader import render_to_string
from . import views


urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('signup/', views.user_registration, name='signup'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	# path('password_change/',
	#   auth_views.PasswordChangeView.as_view(), name='password_change'),
	# path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
	path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='account/registration/password_reset_form.html',
             html_email_template_name='account/registration/password_reset_email.html',
             success_url='/account/password_reset/done/',
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         views.CustomPasswordResetConfirmView.as_view(
             template_name='account/registration/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]
