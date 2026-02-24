from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('base/',views.base,name='base'),
    path('about/',views.about_view,name='about'),
    path('course/',views.course_view,name='course'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/',views.student_profile,name='profile'),
    path('edits/',views.edits,name='edits'),
    path('save_edits/',views.save_edits,name='save_edits'),
    path('purchase_course/<int:id>/',views.purchase_course,name='purchase_course')
]