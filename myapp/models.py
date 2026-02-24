from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    ADMIN = 'admin'
    STUDENT = 'student'
        
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (STUDENT, 'Student'),
    )
    
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES,
    )
    
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    admission_year = models.PositiveIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    def __str__(self):
        return f"{self.username} ({self.role})"

