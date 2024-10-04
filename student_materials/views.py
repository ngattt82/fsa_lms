from subject.models import Material, Subject  # Ensure these are correct
from django.shortcuts import render, get_object_or_404
# from module_group.models import ModuleGroup
from django.http import HttpResponse, FileResponse
import zipfile
import os
import mimetypes
from training_program.models import TrainingProgram
from training_program_subjects.models import TrainingProgramSubjects
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from user.models import Profile
@login_required
def select_material(request):
    # Get the current user
    if request.user.is_authenticated:
        user = request.user
    else:
        # Default to a specific user, e.g., user with ID 4 (or handle anonymous users accordingly)
        user = User.objects.get(pk=4)  # Assuming user with ID 4 is the default or superadmin

    user_profile = get_object_or_404(Profile, user=user)  # Assuming UserProfile is linked to User via ForeignKey
    # Get the training programs assigned to the user
    user_training_programs = user.training_programs.all()

    # Check if a training program has been selected
    training_program_id = request.GET.get('training_program_id')
    training_program = None  # Initialize to None by default

    if training_program_id:
        training_program = get_object_or_404(TrainingProgram, pk=training_program_id)
        # Filter through TrainingProgramSubjects to get the subjects for this training program
        training_program_subjects = TrainingProgramSubjects.objects.filter(program=training_program)
        subjects = Subject.objects.filter(trainingprogramsubjects__in=training_program_subjects)
    else:
        subjects = Subject.objects.all()  # Default to all subjects if no training program is selected

    # Handle subject and material selection logic
    fileSelect = request.GET.get("fileSelect", "assignments")  # Default to 'assignments'
    subject_id = request.GET.get('subject_id')

    # Default to the first subject if none is selected and subjects exist
    if not subject_id and subjects.exists():
        subject_id = subjects.first().id

    if subject_id:
        subject = get_object_or_404(Subject, pk=subject_id)
        materials = Material.objects.filter(subject=subject, material_type=fileSelect)

        # Filter materials by category
        assignments = subject.materials.filter(material_type='assignments')
        labs = subject.materials.filter(material_type='labs')
        lectures = subject.materials.filter(material_type='lectures')
        references = subject.materials.filter(material_type='references')

        # Sort materials by file name
        assignments = sorted(assignments, key=lambda m: m.file.name if m.file else '')
        labs = sorted(labs, key=lambda m: m.file.name if m.file else '')
        lectures = sorted(lectures, key=lambda m: m.file.name if m.file else '')
        references = sorted(references, key=lambda m: m.file.name if m.file else '')
    else:
        subject = None
        materials = None
        assignments = []
        labs = []
        lectures = []
        references = []

    return render(request, 'materials/subject_material.html', {
        'training_programs': user_training_programs,
        'selected_training_program': training_program,  # Pass the selected training program (if any)
        'subjects': subjects,
        'selected_subject': subject,
        'materials': materials,
        'assignments': assignments,
        'labs': labs,
        'lectures': lectures,
        'references': references,
        'fileSelect': fileSelect,  # Pass the selected category to the template
    })


def view_material(request, material_id):
    # Get the material object
    material = get_object_or_404(Material, id=material_id)

    # Get the file path
    file_path = material.file.path
    file_type = material.file.name.split('.')[-1].lower()

    # Define supported types for preview
    supported_types = ['pdf', 'txt', 'xls', 'doc', 'docx']

    if file_type in supported_types:
        # If the file is supported, open it as a FileResponse
        file = open(file_path, 'rb')
        mime_type, _ = mimetypes.guess_type(file_path)
        return FileResponse(file, content_type=mime_type)
    else:
        # If not supported, return an error or download the file instead
        return HttpResponse("Viewing this file type is not supported.", status=400)
    

def download_all_materials(request, material_type):
    zip_filename = f'{material_type}s.zip'
    
    # Create a zip file
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        materials = Material.objects.filter(material_type=material_type)  # Use 'material_type' instead of 'type'
        for material in materials:
            zip_file.write(material.file.path, arcname=os.path.basename(material.file.name))

    # Serve the zip file
    response = HttpResponse(open(zip_filename, 'rb'), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'
    
    # Optionally, delete the zip file after sending it
    # os.remove(zip_filename)
    
    return response