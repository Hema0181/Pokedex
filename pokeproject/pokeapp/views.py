from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

import requests
from django.shortcuts import render

def home(request):
    pokemon_name = request.GET.get('name', 'pikachu')  # Default is pikachu
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        image_url = data['sprites']['front_default']
        context = {
            'name': pokemon_name.capitalize(),
            'image': image_url,
        }
    else:
        context = {
            'name': "Not Found",
            'image': None,
        }

    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
