from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name = 'accounts'

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
	path('logout/', auth_views.LogoutView.as_view(), name="logout"),
	path("password_reset", views.PasswordResetRequest, name="password_reset"),
	path("password_change", auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"), name="password_change"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
	# profile links
	path('views/account_view/', views.AccountView, name="account_view"),
	path('views/profile_view/<slug:username>/', views.profile, name='profile_view'),
	path('views/profile_summary/<str:username>', views.ProfileSummary, name='profile_summary'),
	path('views/profile_edit/<slug:username>', views.EditProfile, name='profile_edit'),

]