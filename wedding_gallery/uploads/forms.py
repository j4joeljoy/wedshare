from django import forms
from gallery.models import Photo

class PhotoUploadForm(forms.ModelForm):
    image_file = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Choose Photo'
    )

    class Meta:
        model = Photo
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Give your photo a title'
            })
        }
