# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import MaterialSelectionForm
from subject.models import Material, Subject  # Ensure these are correct

def select_material(request):
    form = MaterialSelectionForm()
    materials = None

    if request.method == 'POST':
        form = MaterialSelectionForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            material_type = form.cleaned_data['material_type']

            # Filter materials based on the selected subject and type
            materials = Material.objects.filter(subject=subject, material_type__in=['pdf', 'xls', 'doc', 'txt'])

    return render(request, 'select_material.html', {
        'form': form,
        'materials': materials,
    })

def load_files(request):
    subject_id = request.GET.get('subject_id')
    material_type = request.GET.get('material_type')

    files = Material.objects.filter(subject_id=subject_id, material_type__in=['pdf', 'xls', 'doc', 'txt'])
    return JsonResponse(list(files.values('id', 'file_name')), safe=False)
