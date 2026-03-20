from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg, Count
from .models import Package, Profile, Review
from django.contrib import messages

# Create your views here.

def index(request):
    packages = Package.objects.all()
    reviews = Review.objects.all().order_by('-id')[:6]       # latest 6 reviews
    domestic_package = Package.objects.filter(package_type = 'domestic')[:8]
    international_package = Package.objects.filter(package_type = 'international')[:8]
    for p in domestic_package:
        p.stay_list = p.stay_plan.split("•")
        p.avg_rating = Review.objects.filter(package=p).aggregate(
            Avg('rating')
        )['rating__avg']

        p.review_count = Review.objects.filter(package=p).count()


    for p in international_package:
        p.stay_list = p.stay_plan.split("•")
        p.avg_rating = Review.objects.filter(package=p).aggregate(
            Avg('rating')
        )['rating__avg']

        p.review_count = Review.objects.filter(package=p).count()

    north = Package.objects.filter(region='north', package_type='domestic')
    west = Package.objects.filter(region='west', package_type='domestic')
    south = Package.objects.filter(region='south', package_type='domestic')
    northeast = Package.objects.filter(region='northeast', package_type='domestic')

    for p in north:
        p.stay_list = p.stay_plan.split("•")
        p.avg_rating = Review.objects.filter(package=p).aggregate(
            Avg('rating')
        )['rating__avg']

        p.review_count = Review.objects.filter(package=p).count()

    for p in west:
        p.stay_list = p.stay_plan.split("•")
        p.avg_rating = Review.objects.filter(package=p).aggregate(
            Avg('rating')
        )['rating__avg']

        p.review_count = Review.objects.filter(package=p).count()
    
    for p in south:
        p.stay_list = p.stay_plan.split("•")
        p.avg_rating = Review.objects.filter(package=p).aggregate(
            Avg('rating')
        )['rating__avg']

        p.review_count = Review.objects.filter(package=p).count()
    
    for p in northeast:
        p.stay_list = p.stay_plan.split("•")
        p.avg_rating = Review.objects.filter(package=p).aggregate(
            Avg('rating')
        )['rating__avg']

        p.review_count = Review.objects.filter(package=p).count()

    trending_india = Package.objects.filter(is_trending = True)[:8]

    for p in trending_india:
        p.stay_list = p.stay_plan.split("•")
        p.avg_rating = Review.objects.filter(package=p).aggregate(
            Avg('rating')
        )['rating__avg']

        p.review_count = Review.objects.filter(package=p).count()
        
    
    return render(request, 'index.html', {
        'packages': packages, 
        'reviews': reviews, 
        'domestic_package': domestic_package, 
        'international_package':international_package,
        'north': north,
        'west': west,
        'south': south,
        'northeast': northeast,
        'trending_india': trending_india,
        })


# logical part
def package_detail(request, id):
    package = get_object_or_404(Package, id=id)
    return render(request, 'package_detail.html', {'package': package})

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        if User.objects.filter(username = username).exists():
            messages.error(request, "Username already exist")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')
        user = User.objects.create_user(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        Profile.objects.create(
            user = user,
            phone = phone,
        )
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def home(request):
    packages = Package.objects.all()
    return render(request, "home.html", {'packages': packages})






