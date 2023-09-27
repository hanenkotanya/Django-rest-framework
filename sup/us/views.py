from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from django.urls import conf
from django.utils import timezone
from .forms import CustomUserCreationForm, ProfileForm


def index(request):
    return render(request, 'us/index.html')

def registerUser(request):
    page = 'registerUser'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.capitalize()
            user.save()

            messages.success(request, 'Аккаунт успешно создан!')

            login(request, user)
            return redirect('editProfile')
        else:
            messages.success(request, 'Во время регистрации возникла ошибка')

    context = {'page': page, 'form': form}
    return render(request, 'us/registerUser.html', context)

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        profile = request.user.profile
        return redirect('userProfile', slug=profile.slug)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Такого пользователя нет в системе')

        user = authenticate(request, username=username, password=password)

        
        if user is not None:
            login(request, user)
            profile = request.user.profile
            return redirect('userProfile', slug=profile.slug)

        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'us/loginUser.html')


@login_required(login_url='login')
def userProfile(request, slug):
    profile= Profile.objects.get(slug=slug)
    context = {'profile': profile}
    return render(request, 'us/userProfile.html', context)


@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('userProfile')

    context = {'form': form}
    return render(request, 'us/editProfile.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
 
    return redirect('index')