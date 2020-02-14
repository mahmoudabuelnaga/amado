from django.contrib import admin
from . import models

# Register your models here.
class ImageInline(admin.TabularInline):
    model = models.Image
    row_id_fields = ['image']

# class ColorInline(admin.TabularInline):
#     model = models.Color
#     row_id_fields = ['color']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display        = ['title','slug','price','brand','catagory','available']
    list_filter         = ['available','created','updated','catagory','brand','price']
    list_editable       = ['slug','available']
    prepopulated_fields = {'slug': ('title',)}
    inlines             = [ImageInline]

@admin.register(models.Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    list_dispaly        = ['title','slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_dispaly        = ['title','slug']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(models.Image)
admin.site.register(models.Color)
