from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegisterForm

# Create your views here.

def index(request):
    user = request.user
    print(user)
    return render(
        request,
        "back/index.html",
        { "user": user }
    )

@login_required
def profile(request):
    user = request.user
    return render(
        request,
        "back/profile.html",
        { "user": user },
    )

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form, 'title':'Sign Up for Blackhole Megalaser'})
