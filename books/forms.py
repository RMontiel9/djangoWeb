from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe un comentario (opcional)'}),
            'rating': forms.Select()
        }

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        comment = cleaned_data.get('comment')

        # Validación: si hay comentario, debe haber rating válido
        if comment and (rating is None or rating == 0):
            self.add_error('rating', 'Debes seleccionar una valoración si vas a dejar un comentario.')

        return cleaned_data
