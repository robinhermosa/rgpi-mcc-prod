from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import update_session_auth_hash,authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm,AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from . import forms
from . import views
from .models import *
from .forms import UserForm, ProfileForm, UserUpdateForm, ProfileUpdateForm
from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
@admin_only
def registerPage(request):
    if request.method == 'POST':
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST, request.FILES)

        if u_form.is_valid() and p_form.is_valid():
            
            user = u_form.save()
            profile = p_form.save(commit=False)
            profile.user = user
            profile.save()

            fullname = u_form.cleaned_data.get('first_name')+' '+u_form.cleaned_data.get('last_name')
            my_group = Group.objects.get(name=u_form.cleaned_data.get('group')) 
            my_group.user_set.add(user)
             
            messages.success(request, 'Account was successfully created for '+ fullname )

            if request.user.is_authenticated:
                return redirect('account_view')
            else:
                return redirect('login')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return redirect('register')
    else: 
        u_form = UserForm()
        p_form = ProfileForm()
        context = {
                    'u_form': u_form,
                    'p_form': p_form,
                } 
        
        return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in as {username}.")
            return redirect("home")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        context = {}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    if request.session:
        messages.success(request, 'Successfully Logged Out')
    else:
        messages.error(request, 'Session Expired Please Login Again')
    logout(request)	
    return redirect('login')

def PasswordResetRequest(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'https://rgpi-mcc-dashboard.herokuapp.com',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                messages.success(request, 'A message with reset password instructions has been sent to your inbox.')	
                return redirect ("home")
        
        messages.error(request, 'An invalid email has been entered.')
    form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', context={'form':form})

@login_required(login_url='login')
@admin_only
def AccountView(request):
    accounts = User.objects.all()
    return render(request, 'views/account_views.html', {"accounts": accounts} )

@login_required(login_url='login')
def EditProfile(request, username):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile_view',username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'views/account_edit.html',context )

@login_required(login_url='login')
def profile(request , username):
    return render(request, 'views/account_profile.html')

@login_required(login_url='login')
def ProfileSummary(request, username):
    user_summary = User.objects.filter(username = username)
    context = {
        'user_summary': user_summary
    }
    return render(request, 'views/account_summary.html', context)

def get_object(self):
    username= self.kwargs.get("username")
    return get_object_or_404(User, username=username)

# @login_required(login_url='login')
# @admin_only
# def deleteuser(request, username):
# 	user = User.objects.filter(username = username)
# 	user.is_active = False
# 	user.save()
# 	messages.success(username, "Profile successfully disabled.")
# 	return render(request, 'accounts/delete_user.html')
