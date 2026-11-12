from django import forms
from .models import Project, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Full-Stack Django App'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief project summary...'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Add a new task...'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
