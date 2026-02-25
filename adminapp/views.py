from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from .forms import CourseForm
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import Course
from . decorators import admin_required
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
studentdata = get_user_model()
@never_cache

@admin_required
def dashboard(request):
    if request.user.is_authenticated and request.user.role=='admin':
        no_of_course = Course.objects.count()
        no_of_students = studentdata.objects.filter(role ='student').count()
        total_admins = studentdata.objects.filter(role='admin').count()
        numbers={
            'no_of_students':no_of_students,
            'no_of_course':no_of_course,
            'total_admins':total_admins
        }
        return render(request,'adminpage/dashboard.html',numbers)
    else:
        return redirect('login')
@admin_required
def course_list(request):
    courses = Course.objects.all()
    return render(request,'adminpage/courselist.html',{'courses':courses})
@admin_required
def student_list(request):
    students = studentdata.objects.filter(role='student')
    return render(request,'adminpage/students.html',{'students':students})
@admin_required
def add_course(request):
    if request.method=='POST':
        form = CourseForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.error(request,'Added Successfully')
            return redirect('course_list')
        else:
            print(form.errors)
    else:
        form = CourseForm()
    return render(request,'adminpage/addcourse.html',{'form':form})
@admin_required
def student_view(request,id):
    students = studentdata.objects.get(id=id)
    return render(request,'adminpage/studentview.html',{"students":students})
@admin_required
def student_block(request,id):
    student = studentdata.objects.get(id=id)
    student.is_active = False
    student.save()
    subject = 'Account Blocked !'
    message = f'Hi {student.username},\n\n Your account is  Blocked .'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [student.email]
    send_mail(subject, message, email_from, recipient_list)
    messages.success(request,' Account Blocked !')
    return redirect('student_list')
@admin_required
def student_active(request,id):
    student = studentdata.objects.get(id=id)
    student.is_active = True
    student.save()
    subject = 'Account Re-activated !'
    message = f'Hi {student.username},\n\n Your account is  Re-activated .'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [student.email]
    send_mail(subject, message, email_from, recipient_list)
    messages.success(request,' Account Unblocked !')
    return  redirect('student_list')
@admin_required
def student_delete(request,id):
    student = studentdata.objects.get(id=id)
    student_name  = student.username
    student.delete()
    subject = 'Account Deleted !'
    message = f'Hi {student.username},\n\n Your account is Deleted by Admin  .'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [student.email]
    send_mail(subject, message, email_from, recipient_list)
    messages.success(request,f'student {student_name} successfully deleted.')
    return redirect('student_list')

@admin_required
def edit_course(request,id):
    courses = Course.objects.get(id=id)
    return render(request,'adminpage/editcourse.html',{'courses':courses})

@admin_required
def save_edit(request,id):
    courses = Course.objects.get(id=id)
    if request.method=='POST':
        courses.Course_name=request.POST.get('Course_name')
        courses.Course_detail = request.POST.get('Course_detail')
        courses.Course_fee = request.POST.get('Course_fee')
        courses.Course_duration = request.POST.get('Course_duration')
        if request.FILES.get('Course_photo'):
            courses.Course_photo = request.FILES.get('Course_photo')
        courses.save()
        messages.success(request,'Course successfully Edited')
        return redirect('course_list')

@admin_required
def course_delete(request,id):
    item = Course.objects.get(id=id)
    item.delete()
    messages.success(request,'Course deleted Successfully...')
    return redirect('course_list')
