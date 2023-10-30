from django import forms
from ..cms.models import Media

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['file']