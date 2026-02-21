from django.shortcuts import render
from django.contrib.auth.views import LoginView , LogoutView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import User
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
import logging



logger = logging.getLogger(__name__)




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

def error_404(request, exception=None):
    """
    Handle 404 errors
    """
    logger.warning(f'404 error: {request.path} - {exception}')
    context = {
        'error_code': 404,
        'custom_message': 'The page you are looking for might have been moved or deleted.'
    }
    return render(request, 'base/bugs/oops.html', context, status=404)

def error_500(request):
    """
    Handle 500 errors
    """
    logger.error(f'500 error on {request.path}')
    context = {
        'error_code': 500,
        'custom_message': 'Something went wrong on our servers. Please try again later.'
    }
    return render(request, 'base/bugs/oops.html', context, status=500)

def error_403(request, exception=None):
    """
    Handle 403 errors
    """
    logger.warning(f'403 error: {request.path} - {exception}')
    context = {
        'error_code': 403,
        'custom_message': 'You do not have permission to access this page.'
    }
    return render(request, 'base/bugs/oops.html', context, status=403)

def error_400(request, exception=None):
    """
    Handle 400 errors
    """
    logger.warning(f'400 error: {request.path} - {exception}')
    context = {
        'error_code': 400,
        'custom_message': 'Your browser sent a request that this server could not understand.'
    }
    return render(request, 'base/bugs/oops.html', context, status=400)

def oops_page(request):
    """
    Direct URL for accessing the oops page manually
    """
    return render(request, 'base/bugs/oops.html')