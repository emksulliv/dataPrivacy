from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    pass
    return render(request, 'index.html', {})
