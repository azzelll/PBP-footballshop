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
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='shoes')
    
    stock = models.IntegerField(default=0)
    sizes = models.CharField(max_length=100, blank=True, help_text="Separate sizes with commas, e.g., 39,40,41 or S,M,L,XL")
    
    discount = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    
    rating = models.FloatField(default=0.0)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.name

    @property
    def final_price(self):
        """Calculate price after discount"""
        return self.price * (1 - (self.discount / 100))

    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0

    def full_name(self):
        """Return brand + product name"""
        return f"{self.brand} {self.name}"

    def get_sizes_list(self):
        """Return list of sizes from comma-separated string"""
        if self.sizes:
            return [size.strip() for size in self.sizes.split(',')]
        return []
    
    def has_size(self, size):
        """Check if product has specific size"""
        return size in self.get_sizes_list()
    
    @property
    def sizes_display(self):
        """Display formatted sizes (truncate if too many)"""
        sizes = self.get_sizes_list()
        if len(sizes) > 4:
            return f"{', '.join(sizes[:4])} +{len(sizes)-4} more"
        return ', '.join(sizes) if sizes else "One Size"

    def formatted_price(self):
        """Return formatted price in Indonesian Rupiah"""
        price = int(self.final_price)
        return f"Rp {price:,}".replace(",", ".")
    
    class Meta:
        ordering = ['-created_at']  # Newest first
        verbose_name = "Product"
        verbose_name_plural = "Products"