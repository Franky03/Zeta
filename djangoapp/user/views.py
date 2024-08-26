from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        #verificação de usuario
        if not username or not email or not password1 or not password2:
            messages.error(request, 'Please fill in all fields.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create(username=username, email=email, password=make_password(password1))
            user.save()
            return redirect('/')
        
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  # Verifique se o usuário existe no banco de dados
        if user is not None:
            auth_login(request, user)
            return redirect('/')  # Redirecione para a página inicial
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

def pageUser(request):
    if request.user.is_authenticated:
        return render(request, 'pageUser.html')
    else:
        return redirect('login')
