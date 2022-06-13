from django.shortcuts import render

# Create your views here.


def deployment(request):
    return render(request, 'node/deployment.html')