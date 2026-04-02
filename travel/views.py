from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg, Count
from .models import Package, Profile, Review, Booking
from django.contrib import messages
from django.db.models import Q
from .models import Package


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
    similar_packages = Package.objects.filter(location=package.location,package_type=package.package_type).exclude(id=package.id)[:4]

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
       

        messages.success(request, "Enquiry submitted successfully!")

        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")

        date = request.POST.get("date")
        persons = int(request.POST.get("persons"))

        total_price = persons * package.price

        Booking.objects.create(
            user=request.user,
            package=package,
            booking_date=date,
            persons=persons,
            total_price=total_price
        )

        messages.success(request, "Booking confirmed successfully!")
        return redirect('package_detail', id=id)

    # Stay plan list
    package.stay_list = package.stay_plan.split("•") if package.stay_plan else []

    # Reviews
    reviews = Review.objects.filter(package=package).order_by('-id')[:3]
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating or 0)
    review_count = reviews.count()

    #  Convert itinerary into day-wise list
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
        'similar_packages': similar_packages,
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
        next_url = request.POST.get("next")  # 🔥 IMPORTANT

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if next_url:
                return redirect(next_url)

            return redirect('home')

        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("home_page")

def home(request):
    packages = Package.objects.all()
    return render(request, "home.html", {'packages': packages})

def search_packages(request):
    query = request.GET.get('q')

    results = []

    if query:
        results = Package.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'query': query,
        'results': results
    }

    return render(request, 'search_results.html', context)








# helper function---------------->
def prepare_packages(packages):
    for p in packages:
        p.stay_list = p.stay_plan.split("•") if p.stay_plan else []

        reviews = Review.objects.filter(package=p)
        p.avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        p.review_count = reviews.count()

    return packages






