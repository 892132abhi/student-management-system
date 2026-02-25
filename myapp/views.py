from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from adminapp.models import Course
from django.core.mail import send_mail
from . decorators1 import student_required
from django.conf import settings
# Create your views here.
@never_cache
def home(request):
    courses = Course.objects.count()
    return render(request,'student/home.html',{'courses':courses})
@never_cache
def login_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                if user.role.lower()=='admin' and request.user.is_authenticated:
                    return redirect('dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request,'Admin Blocked your Acccount...')
    return render(request,'student/login.html')
@never_cache
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.save()

            subject = 'Welcome to SLMS'
            message = f'Hi {user.username},\n\nYour account has been created successfully. You can now login to the Student Learning Management System.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                print(f"Email failed: {e}") 

            messages.success(request, 'Account created successfully! A confirmation email has been sent.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'student/register.html', {'form': form})

def base(request):
    if request.user.is_active:
        return render(request,'student/base.html')
    messages.success(request,'Account Blocked !')
    return redirect('login')
@never_cache
def about_view(request):
    return render(request,'student/about.html')

@login_required
def course_view(request):
    if request.user.is_active:
        courses = Course.objects.all()
        return render(request,'student/courses.html',{'courses':courses})
    else:
        return redirect('login')

@student_required
def student_profile(request):
    return render(request,'student/profile.html')


def logout_view(request):
    logout(request)
    return redirect('home')

@student_required
def edits(request):
    return render(request,'student/edit.html')

@student_required
def save_edits(request):
    if request.method == 'POST':
        student = request.user
        student.username = request.POST.get('username')
        student.email = request.POST.get('email')
        student.date_of_birth = request.POST.get('date_of_birth')
        
        if 'profile_pic' in request.FILES:
            student.profile_pic = request.FILES['profile_pic']
            
        
        student.save()
        subject = 'Profile Edited !'
        message = f'Hi {student.username},\n\n Your account has been Edited .'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [student.email]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    
    return redirect('edits')
@student_required
def purchase_course(request,id):
    course_obj = Course.objects.get(id=id)
    if request.method == 'GET' or request.method == 'POST':
        student = request.user
        if student.course is None:
            student.course = course_obj.Course_name
            student.save()
            subject = 'Course Purchase'
            message = f'Hi {request.user.username},\n\n You succesfylly{course_obj.Course_name} purchased .'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, f'Course "{course_obj.Course_name}" added successfully!')
            return redirect('course')
    messages.error(request, f'Already taken 1 Course')
    return redirect('course')
