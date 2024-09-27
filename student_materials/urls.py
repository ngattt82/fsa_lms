from django.urls import path
from . import views

app_name = 'student_materials'

urlpatterns = [
    path('materials/', views.select_material, name='select_material'),
     path('materials/download/all/<str:material_type>/', views.download_all_materials, name='download_all_materials'),
    path('materials/view/<int:material_id>/', views.view_material, name='view_material'),
]
