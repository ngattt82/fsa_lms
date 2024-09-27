from django import forms
from .models import TrainingProgram
from user.models import CustomUser

# Form for creating and editing training programs
class TrainingProgramForm(forms.ModelForm):
    class Meta:
        model = TrainingProgram
        fields = ['program_name', 'program_code', 'description']



