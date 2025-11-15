from django import forms
from .models import Journal

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['title', 'author', 'department', 'abstract', 'keywords', 'pdf_file']
