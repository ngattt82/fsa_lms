from django import forms
from .models import CustomUser, Role
from training_program.models import TrainingProgram

# Form for creating and editing users
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'full_name', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

# Form for creating and editing roles
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name']
        
# TEST1----------------------------------------------------------------
class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label="Upload Excel File")


class AssignTrainingProgramForm(forms.ModelForm):
    training_programs = forms.ModelMultipleChoiceField(
        queryset=TrainingProgram.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['training_programs']

