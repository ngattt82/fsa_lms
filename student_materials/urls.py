from django.urls import path
from .views import select_material
from .views import select_material, load_files

app_name = 'student_materials'

urlpatterns = [
    path('select-material/', select_material, name='select_material'),
    path('ajax/load-files/', load_files, name='ajax_load_files'),
]