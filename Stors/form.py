from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    thumbnail = forms.ImageField(label='Images')
    thumbnail.widget.attrs.update(
        {
            'multiple': True
        }
    )
    
    class Meta:
        model = Product
        fields = '__all__'