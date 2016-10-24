from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse


def error404(request):
    return render(request, '404.html', status=404)
