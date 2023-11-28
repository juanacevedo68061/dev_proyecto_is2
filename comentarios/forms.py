from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    id_texto = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 2, 'style': 'font-family: Helvetica; border: none; outline: none; resize: none; overflow-y: auto; max-height: 10em;', 'placeholder': '¿Qué piensas?'}),
        }
        labels = {
            'texto': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_texto'].widget.attrs['id'] = 'id_texto'
