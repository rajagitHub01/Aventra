from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg, Count
from .models import Package, Profile, Review, Booking
from django.contrib import messages
from django.db.models import Q
from .models import Package
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


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

        form_type = request.POST.get("form_type")

        # ---------------- ENQUIRY ----------------
        if form_type == "enquiry":
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            message = request.POST.get("message")

            messages.success(request, "Enquiry submitted successfully!")
            return redirect('package_detail', id=id)


        # ---------------- BOOKING ----------------
        elif form_type == "booking":

            if not request.user.is_authenticated:
                return redirect(f"/login/?next={request.path}")

            date = request.POST.get("date")
            persons = request.POST.get("persons")

            return redirect(
                f"/booking/start/{package.id}/?date={date}&persons={persons}"
            )

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

def start_booking(request, id):
    package = get_object_or_404(Package, id=id)

    date = request.GET.get("date")
    persons = request.GET.get("persons")

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        return redirect(
            f"/booking/payment/{id}/?date={date}&persons={persons}&name={name}&email={email}&phone={phone}"
        )

    total_price = int(persons) * package.price

    context = {
        "package": package,
        "date": date,
        "persons": persons,
        "total_price": total_price
    }

    return render(request, "booking.html", context)

def payment_page(request, id):
    package = get_object_or_404(Package, id=id)

    date = request.GET.get("date")
    persons = int(request.GET.get("persons"))
    name = request.GET.get("name")
    email = request.GET.get("email")
    phone = request.GET.get("phone")

    total_price = persons * package.price

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create({
        "amount": int(total_price * 100),
        "currency": "INR",
        "payment_capture": 1
    })
    context = {
        "package": package,
        "date": date,
        "persons": persons,
        "name": name,
        "email": email,
        "phone": phone,
        "total_price": total_price,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "order_id": order["id"]
    }

    return render(request, "payment.html", context)
@csrf_exempt
def verify_payment(request):

    if request.method == "POST":

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        data = {
            'razorpay_payment_id': payment_id,
            'razorpay_order_id': order_id,
            'razorpay_signature': signature
        }

        try:
            client.utility.verify_payment_signature(data)

            # save booking after payment success
            package_id = request.POST.get("package_id")
            persons = int(request.POST.get("persons"))
            date = request.POST.get("date")
            total_price = request.POST.get("total_price")

            package = Package.objects.get(id=package_id)

            Booking.objects.create(
                user=request.user,
                package=package,
                booking_date=date,
                persons=persons,
                total_price=total_price,
                status="paid",
                razorpay_payment_id=payment_id,
                razorpay_order_id=order_id
            )

            return redirect("booking_success")

        except:
            return redirect("payment_failed")

def booking_success(request):
    return render(request, "booking_success.html")










# helper function---------------->
def prepare_packages(packages):
    for p in packages:
        p.stay_list = p.stay_plan.split("•") if p.stay_plan else []

        reviews = Review.objects.filter(package=p)
        p.avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        p.review_count = reviews.count()

    return packages






