from django import forms
from main.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'description', 'price', 
                  'discount', 'stock', 'rating', 'sizes', 'thumbnail', 'is_featured']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-colors',
                'placeholder': 'e.g., Predator Elite FG'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-colors',
                'placeholder': 'e.g., Adidas, Nike, Puma'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-colors'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-colors resize-vertical',
                'rows': 5,
                'placeholder': 'Describe the product features, materials, technology, etc.'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-colors',
                'placeholder': '500000',
                'min': 0
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-colors',
                'placeholder': '0',
                'min': 0,
                'max': 100
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-colors',
                'placeholder': '10',
                'min': 0
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-colors',
                'placeholder': '4.5',
                'min': 0,
                'max': 5,
                'step': 0.1
            }),
            'sizes': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-colors',
                'placeholder': 'e.g., 39, 40, 41, 42 or S, M, L, XL'
            }),
            'thumbnail': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-colors',
                'placeholder': 'https://example.com/image.jpg'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500'
            })
        }
        
        labels = {
            'name': 'Product Name',
            'brand': 'Brand',
            'category': 'Category',
            'description': 'Description',
            'price': 'Price (Rp)',
            'discount': 'Discount (%)',
            'stock': 'Stock',
            'rating': 'Rating (0-5)',
            'sizes': 'Available Sizes',
            'thumbnail': 'Thumbnail Image URL',
            'is_featured': 'Mark as Featured Product'
        }
        
        help_texts = {
            'sizes': 'Separate multiple sizes with commas',
            'thumbnail': 'Enter a valid image URL',
            'discount': 'Enter discount percentage (0-100)',
            'rating': 'Enter rating from 0 to 5'
        }