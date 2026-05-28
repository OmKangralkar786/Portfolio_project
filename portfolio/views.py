from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PortfolioForm, FeedbackForm
from .models import Portfolio, Feedback, Company

# ✅ Company List
def company_list(request):
    companies = Company.objects.all()  # Fetch all companies from the database
    return render(request, "portfolio/company_list.html", {"companies": companies})

# ✅ User Registration
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")

    return render(request, "portfolio/register.html")

# ✅ User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")  # Redirect to Home Page
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "portfolio/login.html")

# ✅ User Logout
def user_logout(request):
    logout(request)
    return redirect("login")

# ✅ Home Page (After Login)
@login_required
def home(request):
    return render(request, "portfolio/home.html")

# ✅ Employee Dashboard View
def dashboard(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)  # Ensure portfolio exists

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)  # Bind form to existing portfolio
        if form.is_valid():
            form.save()
            return redirect('view_portfolio')  # Redirect to View Portfolio after saving
    else:
        form = PortfolioForm(instance=portfolio)  # Load existing data in form

    return render(request, 'portfolio/dashboard.html', {'form': form})

# ✅ View Personal Portfolio

def view_portfolio(request):
    portfolio = Portfolio.objects.filter(user=request.user).first()  # Get first portfolio if exists
    if not portfolio:
        return render(request, 'portfolio/no_portfolio.html')  # Show a message if no portfolio exists
    return render(request, 'portfolio/view_portfolio.html', {'portfolio': portfolio})

# ✅ Company Form Submission
@login_required
def company_form(request):
    if request.method == "POST":
        company_name = request.POST["company_name"]
        required_skills = request.POST["required_skills"]
        experience = request.POST["experience"]
        address = request.POST["address"]
        contact_number = request.POST["contact_number"]

        messages.success(request, "Company details submitted successfully!")
        return redirect("home")

    return render(request, "portfolio/company_form.html")

# ✅ Admin Check Function
def is_admin(user):
    return user.is_superuser

# ✅ Admin Login View
def admin_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")  # Redirect to Admin Dashboard
        else:
            messages.error(request, "Invalid Admin Credentials")
    return render(request, "portfolio/admin_login.html")

# ✅ Admin Logout View
@login_required
@user_passes_test(is_admin)
def admin_logout(request):
    logout(request)
    return redirect("admin_login")


# ✅ Admin Dashboard - Search Companies by Skill

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    users = User.objects.all()
    portfolios = Portfolio.objects.all()  # Get all portfolios for user details
    companies = Company.objects.all()  # Get all companies

    query = request.GET.get("search")  # Get the search term from the input field

    user_count = 0  # Initialize user count
    company_count = 0  # Initialize company count

    # Filter Users by Skill
    if query:
        portfolios = portfolios.filter(skills__icontains=query)  # Filter user portfolios by skill
        users = [portfolio.user for portfolio in portfolios]  # Extract users from filtered portfolios
        user_count = len(users)

        # Filter Companies by Skill
        companies = companies.filter(required_skills__icontains=query)  # Filter companies by skill
        company_count = companies.count()

    return render(request, "portfolio/admin_dashboard.html", {
        "users": users,
        "portfolios": portfolios,  
        "user_count": user_count,
        "companies": companies,
        "company_count": company_count,
        "query": query,  # Pass search query back to the template
    })

    
# ✅ Admin View User's Portfolio
@user_passes_test(is_admin)
def admin_view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    portfolio = Portfolio.objects.filter(user=user).first()  

    if not portfolio:
        messages.error(request, f"No portfolio found for {user.username}")
        return redirect("admin_dashboard")

    return render(request, "portfolio/admin_view_user.html", {"user": user, "portfolio": portfolio})

# ✅ About Us Page
def about_us(request):
    return render(request, "portfolio/about_us.html")

# ✅ Feedback Submission
@login_required
def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect("home")  
    else:
        form = FeedbackForm()

    return render(request, "portfolio/feedback.html", {"form": form})
