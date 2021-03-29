from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect 
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import views

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = "index.html"

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        messages.info(request, "You are now logged in as {username}.")
        return render(request, 'home')
    else:
        return render(request, 'login')
