from django.shortcuts import render
from django.contrib.auth.views import LoginView , LogoutView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import User
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages


def home(request):
    return render(request,'base/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to DjangoApp.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/auth/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name="users/auth/login.html"
    def get_success_url(self):
        return reverse_lazy('home')
    
class CustomLogoutView(LogoutView):
    next_page=reverse_lazy('login')

def profile(request , user_id):
    user=get_object_or_404(
        User,
        id=user_id,
        )
    return render(
        request,
        'users/profile.html',
        {
            'user':user,
        })