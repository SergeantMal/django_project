from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def data(request):
    return render(request, 'data.html')

def test(request):
    return render(request, 'test.html')