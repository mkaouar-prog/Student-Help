from django import forms
from core.models import Post,Category

class PostCreateForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ('text', 'image', 'categories')
        
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Offre / Demande',
                'id': 'text-input',
                'value' :''
                
            }),
        }
