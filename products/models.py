from django.db import models
from colorfield.fields import ColorField
from django.db.models import Avg, Max, Min
from django.urls import reverse

# Create your models here.
# CATAGORY_CHOICES = (
#     ('C','Chairs'),
#     ('B','Beds'),
#     ('A','Accesories'),
#     ('F','Furniture'),
#     ('HD','Home Decor'),
#     ('D','Dressings'),
#     ('T','Tables'),
#     ('P','Popular'),
# )

class Catagory(models.Model):
    title       = models.CharField(max_length=200, db_index=True)
    slug        = models.SlugField(max_length=200, unique=True)
    image       = models.ImageField(upload_to='catagory/%y/%m/%d')

    class Meta:
        ordering            = ('title',)
        verbose_name        = 'catagory'
        verbose_name_plural = 'catagories'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("products:catagory_detail", kwargs={"slug": self.slug})
    
    
    @property
    def current_price(self):
        if self.products.all():
            return self.products.order_by('price')[0].price
    

class Image(models.Model):
    image       = models.ImageField(upload_to='products/%y/%m/%d')
    product     = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return str(self.id)

class Color(models.Model):
    color       = ColorField(default='#FF0000')

    def __str__(self):
        return str(self.color)


class Brand(models.Model):
    title       = models.CharField(max_length=200, db_index=True)
    slug        = models.SlugField(max_length=200, db_index=True)

    def __str__(self):
        return self.title
        

class Product(models.Model):
    catagory    = models.ForeignKey(Catagory, on_delete=models.CASCADE, related_name='products')
    brand       = models.ForeignKey(Brand, on_delete=models.CASCADE)
    title       = models.CharField(max_length=200, db_index=True)
    slug        = models.SlugField(max_length=200, db_index=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    color       = models.ManyToManyField(Color)
    available   = models.BooleanField(default=True)
    description = models.TextField(db_index=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)


    class Meta:
        ordering        = ('-created',)
        index_together  = (('id','slug'),) 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.pk,"slug":self.slug})
    
    
    @property
    def product_image(self):
        if self.images.all():
            return self.images.order_by('id')[0].image

    @property
    def hover_image(self):
        if self.images.all():
            return self.images.order_by('id')[1].image