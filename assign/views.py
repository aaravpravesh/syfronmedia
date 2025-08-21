
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from datetime import datetime
from .forms import SubmissionForm, ContactForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import transaction
from .models import Assignment, Profile, Submission
from django.contrib.auth import get_user_model
from django.http import JsonResponse


# Create your views here.

def home(request):
    return render(request, 'assign/home.html')


def about(request):
    return render(request, 'assign/about.html')


def website_designing(request):
    return render(request, "assign/website_designing.html")


def ecommerce_solutions(request):
    return render(request, "assign/ecommerce_solutions.html")


def digital_marketing(request):
    return render(request, "assign/digital_marketing.html")

def ppc_campaigns(request):
    return render(request, "assign/ppc_campaigns.html")

def data_science(request):
    return render(request, "assign/data_science.html")

def business_intelligence(request):
    return render(request, "assign/business_intelligence.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("dashboard")  # ✅ redirect to dashboard
            else:
                # ✅ User exists but not active yet
                messages.error(request, "Your account has been created but not approved yet by the admin. Please wait for approval.")
        else:
            messages.error(request, "Invalid username or password")
                  
    return render(request, 'assign/login.html')



@login_required
def dashboard(request):
    assignments = Assignment.objects.filter(user=request.user)
    return render(request, 'assign/dashboard.html', {'assignments': assignments})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def assignment_detail(request, day):
    assignment = get_object_or_404(Assignment, day=day)

    # Get or create submission for this user
    submission, created = Submission.objects.get_or_create(
        assignment=assignment,
        user=request.user
    )

    if request.method == "POST":
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.status = 1  # mark as Submitted
            submission.save()
            return redirect("assignment_detail", day=day)
    else:
        form = SubmissionForm(instance=submission)

    return render(request, "assign/assignment_detail.html", {
        "assignment": assignment,
        "form": form,
        "submission": submission
    })

@login_required
def assignment_list(request):
    assignments = Assignment.objects.all().order_by("day")
    submissions = {s.assignment_id: s for s in Submission.objects.filter(user=request.user)}

    # Build a list with assignment + status
    assignment_data = []
    for assignment in assignments:
        submission = submissions.get(assignment.id)
        status = submission.status if submission else 0  # default "Not Submitted"
        assignment_data.append({
            "assignment": assignment,
            "status": status,
        })

    return render(request, "assign/assignment_list.html", {
        "assignment_data": assignment_data,
    })


@login_required(login_url='/')
def PROFILE(request):
    user = User.objects.get(id=request.user.id)

    context = {
        "user": user,
    }
    return render(request, 'assign/profile.html', context)


@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            customuser = User.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            if password != None and password != "":
                customuser.set_password(password)

            customuser.save()
            profile = Profile.objects.get(user=request.user)
            if profile_pic:
                profile.profile_pic = profile_pic
            profile.save()
            messages.success(request, 'Your Profile Updates Successfully!')
            return redirect('profile')
        except:
            messages.error(request, 'Failed to update your Profile! Please check image size not more than 50kb')
    return render(request, 'assign/profile.html')


User = get_user_model()

def Application(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        resume = request.FILES.get('resume')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        qualification = request.POST.get('qualification')
        dob_str = request.POST.get('dob')

        # ✅ Email and Username check
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken!')
            return redirect('application')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken!')
            return redirect('application')

        # ✅ Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            password=password
        )
        user.is_active = False
        user.save()

        # ✅ Get related profile (auto-created by signal)
        profile = user.profile  

        # ✅ Fix DOB parsing (YYYY-MM-DD from <input type="date">)
        dob = None
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Invalid date format for DOB.")

        # ✅ Save profile data (⚠️ no commas!)
        profile.mobile = mobile
        profile.skills = skills
        profile.experience = experience
        profile.fname = fname
        profile.mname = mname
        profile.dob = dob
        profile.qualification = qualification
        if profile_pic:
            profile.profile_pic = profile_pic
        if resume:
            profile.resume = resume
        profile.save()

        # ✅ Success message
        messages.success(
            request,
            f"Dear {user.first_name}, your application has been submitted successfully! Wait for admin approval."
        )
        return redirect('login')

    return render(request, 'assign/subscription.html')


User = get_user_model()

def check_username(request):
    username = request.GET.get("username", None)
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})

def check_email(request):
    email = request.GET.get("email", None)
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Email send
            send_mail(
                subject=f"New Contact Form Submission: {contact.subject}",
                message=f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}",
                from_email="syfronmedia@gmail.com",  # 👈 yaha apna email daalna
                recipient_list=["syfronmedia@gmail.com"],  # 👈 yaha destination email daalna
                fail_silently=False,
            )

            messages.success(request, "✅ Your message has been sent successfully to Syfron Media! We will contact to you soon. Thanks for your Patience!")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "assign/contact.html", {"form": form})
