import datetime

from django import forms
from api.models import Task

class TaskManagerForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get("due_date")

        if due_date < datetime.date.today():
            raise forms.ValidationError("Due date cannot be in the past")

