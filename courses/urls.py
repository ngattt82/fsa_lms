from django.urls import path
from . import views


app_name = 'courses'

urlpatterns = [
    path('course', views.course_list, name='course_list'),
    path('import/', views.import_courses, name='import_courses'),
    path('delete-courses/', views.delete_courses, name='delete_courses'),
]
