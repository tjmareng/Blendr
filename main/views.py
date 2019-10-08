from django.shortcuts import render
from django.http import HttpResponse

# Views
from Blendr.firebase_config import db


def homepage(request):



    # data = {"name": "testboy"}
    # db.child("test").push(data)

    return HttpResponse("Hello")
