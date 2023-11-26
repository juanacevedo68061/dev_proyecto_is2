from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 1, 'style': 'border: none; outline: none; resize: none; overflow: hidden;', 'placeholder': '¿Qué piensas?'}),
        }
        labels = {
            'texto': '',  # Deja el label vacío para que no se muestre
        }
