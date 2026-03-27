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

    europe = prepare_packages(
    Package.objects.filter(region_international='europe', package_type='international')
    )

    southeast_asia = prepare_packages(
        Package.objects.filter(region_international='southeast_asia', package_type='international')
    )

    middle_east = prepare_packages(
        Package.objects.filter(region_international='middle_east', package_type='international')
    )

    maldives = prepare_packages(
        Package.objects.filter(region_international='maldives', package_type='international')
    )

    usa = prepare_packages(
        Package.objects.filter(region_international='usa', package_type='international')
    )

    dubai = prepare_packages(
        Package.objects.filter(region_international='dubai', package_type='international')
    )
    
        
    
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
        'europe': europe,
        'southeast_asia': southeast_asia,
        'middle_east': middle_east,
        'maldives': maldives,
        'usa': usa,
        'dubai': dubai,
        })


# logical part
def package_detail(request, id):
    package = get_object_or_404(Package, id=id)
    images = package.images.all()[:6]
    highlights = package.highlights_list.all()[:5]
    itinerary_days = package.itinerary_days.all().order_by('day_number')
    inclusions = package.inclusions_list.all()
    exclusions = package.exclusions_list.all()

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
       

        messages.success(request, "Enquiry submitted successfully!")

    # Stay plan list
    package.stay_list = package.stay_plan.split("•") if package.stay_plan else []

    # Reviews
    reviews = Review.objects.filter(package=package).order_by('-id')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    review_count = reviews.count()

    # 🔥 Convert itinerary into day-wise list
    itinerary_days = package.itinerary_days.all().order_by('day_number')



    context = {
        'package': package,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
        'itinerary_days': itinerary_days,
        'images': images,
        'highlights': highlights,
        'inclusions': inclusions,
        'exclusions': exclusions,
    }

    return render(request, 'package_detail.html', context)

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

# helper function---------------->
def prepare_packages(packages):
    for p in packages:
        p.stay_list = p.stay_plan.split("•") if p.stay_plan else []

        reviews = Review.objects.filter(package=p)
        p.avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        p.review_count = reviews.count()

    return packages






