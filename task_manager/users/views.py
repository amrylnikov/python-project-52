from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def index(request):
    return render(request, 'users.html')


def login(request):
    return render(request, 'login.html')
