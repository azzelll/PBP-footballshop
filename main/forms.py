from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'brand',
            'description',
            'thumbnail',
            'category',
            'price',
            'discount',
            'is_featured',
        ]