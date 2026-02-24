from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def login_page(request):
    if request.user.is_authenticated:
        return redirect('products')
    return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('products')
        else:
            messages.error(request, 'Неверный логин или пароль.')
            return redirect('login_page')
    return redirect('login_page')


def register_view(request):
    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not full_name or not password1:
            messages.error(request, 'Все поля обязательны.')
            return redirect('/login/?tab=register')
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('/login/?tab=register')
        if len(password1) < 6:
            messages.error(request, 'Пароль должен быть не менее 6 символов.')
            return redirect('/login/?tab=register')
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Пользователь «{username}» уже существует.')
            return redirect('/login/?tab=register')

        parts = full_name.split()
        user = User.objects.create_user(
            username=username,
            password=password1,
            last_name=parts[0] if len(parts) > 0 else '',
            first_name=parts[1] if len(parts) > 1 else '',
        )
        login(request, user)
        return redirect('products')
    return redirect('login_page')


def guest_view(request):
    request.session['is_guest'] = True
    return redirect('products')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login_page')


def products_view(request):
    is_guest = request.session.get('is_guest', False)
    if not request.user.is_authenticated and not is_guest:
        return redirect('login_page')
    context = {
        'username': request.user.get_full_name() or request.user.username if request.user.is_authenticated else 'Гость'
    }
    return render(request, 'products.html')