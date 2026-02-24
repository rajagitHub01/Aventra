from django.shortcuts import render, get_object_or_404
from .models import Package

# Create your views here.

def home(request):
    packages = Package.objects.all()
    return render(request, 'index.html', {'packages': packages})

def package_detail(request, id):
    package = get_object_or_404(Package, id=id)
    return render(request, 'package_detail.html', {'package': package})
