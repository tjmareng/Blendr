from django.shortcuts import render
from django.http import HttpResponse

# Views
from Blendr.firebase_config import db


def index(request):
    # data = {"name": "testboy"}
    # db.child("test").push(data)

    return render(request, 'main/index.html')


def login(request):
    return render(request, 'main/login.html')
