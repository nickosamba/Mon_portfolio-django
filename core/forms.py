from django import forms
from .models import Commentaire

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['nom', 'message']
        widgets = {
        'nom': forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-900 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Votre nom'
        }),
        'message': forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-900 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Votre message...'
        }),
}

