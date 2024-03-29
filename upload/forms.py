from django import forms
from .models import Sound

class SoundForm(forms.ModelForm):
    class Meta:
        model = Sound
        fields = ["title","category","soundfile"]
        widgets = {'created_by': forms.HiddenInput()}
        file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
