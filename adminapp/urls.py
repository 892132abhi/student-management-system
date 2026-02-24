from django.urls import path
from . import views

urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    path('courselist/',views.course_list,name='course_list'),
    path('student_list/',views.student_list,name='student_list'),
    path('add_course/',views.add_course,name='add_course'),
    path('student_view/<int:id>/',views.student_view,name='student_view'),
    path('student_block/<int:id>/',views.student_block,name='student_block'),
    path('student_active/<int:id>/',views.student_active,name='student_active'),
    path('student_delete/<int:id>/',views.student_delete,name='student_delete'),
    path('edit_course/<int:id>/',views.edit_course,name='edit_course'),
    path('save_edit/<int:id>/',views.save_edit,name='save_edit'),
    path('course_delete/<int:id>/',views.course_delete,name='course_delete')
]