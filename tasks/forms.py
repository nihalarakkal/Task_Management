from django import forms
from .models import Task, User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CompletionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['completion_report', 'worked_hours']
        widgets = {
            'completion_report': forms.Textarea(attrs={'rows':3, 'class':'form-control'}),
            'worked_hours': forms.NumberInput(attrs={'class':'form-control', 'min':0}),
        }

    def clean(self):
        cleaned_data = super().clean()
        completion_report = cleaned_data.get("completion_report")
        worked_hours = cleaned_data.get("worked_hours")

        if not completion_report:
            self.add_error('completion_report', "Completion report is required.")
        if worked_hours is None:
            self.add_error('worked_hours', "Worked hours is required.")
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
