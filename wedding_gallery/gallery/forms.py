from django import forms
from .models import PhotoComment

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control bg-transparent text-white', 
            'rows': 3, 
            'placeholder': 'Write a lovely comment...',
            'style': 'border: 1px solid rgba(255,255,255,0.3);'
        }),
        label=''
    )

    class Meta:
        model = PhotoComment
        fields = ['comment']
