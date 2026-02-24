from django.db import models
# Create your models here.

class Course(models.Model):
    Course_name = models.CharField(max_length=200,null=True)
    Course_detail = models.TextField(blank=True,null=True)
    Course_fee = models.DecimalField(max_digits=10,decimal_places=2)
    Course_duration = models.CharField(max_length=50)
    Course_photo = models.ImageField(upload_to='course_photos/', null=True, blank=True)
    def __str__(self):
        return f"{self.Course_name}"