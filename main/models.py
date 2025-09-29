import uuid
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('shoes', 'Sepatu'),
        ('clothing', 'Pakaian'),
        ('gear', 'Gear (Bola, Pelindung, Alat Latihan)'),
        ('accessories', 'Aksesoris'),
        ('lifestyle', 'Lifestyle / Merchandise'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=50)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    
    stock = models.IntegerField(default=0)
    sizes = models.CharField(max_length=100, blank=True)
    
    discount = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    
    rating = models.FloatField(default=0.0)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    @property
    def final_price(self):
        return self.price * (1 - (self.discount / 100))

    def is_in_stock(self):  
        return self.stock > 0

    def full_name(self):
        return f"{self.brand} {self.name}"

    def list_sizes(self):
        return ", ".join([size.name for size in self.sizes.all()])

    def formatted_price(self):
        return f"Rp {self.final_price:,.0f}".replace(",", ".")

