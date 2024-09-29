from django.urls import path
from . import views

app_name = 'student_materials'

urlpatterns = [
    path('materials/', views.select_material, name='select_material'),
    path('materials/download/all/<str:material_type>/', views.download_all_materials, name='download_all_materials'),
    path('materials/view/<int:material_id>/', views.view_material, name='view_material'),
    
    path('view_pdf/<path:google_drive_link>/', views.view_pdf, name='view_pdf'),
     # AJAX endpoints
    path('api/training_programs/<int:training_program_id>/subjects/', views.get_subjects, name='get_subjects'),
    path('api/subjects/<int:subject_id>/material_types/', views.get_material_types, name='get_material_types'),
]
