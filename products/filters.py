from .models import Product, Catagory, Image, Color, Brand
import django_filters
from django import forms


class ProductFilter(django_filters.FilterSet):
    catagory = django_filters.ModelMultipleChoiceFilter(
        queryset = Catagory.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs={
            'class':'form-check-label',
        })
    )

    brand = django_filters.ModelMultipleChoiceFilter(
        queryset = Brand.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs={
            'class':'form-check-label',
            
        })
    )

    color = django_filters.ModelMultipleChoiceFilter(
        queryset = Color.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs={
            
            'class':'form-check-label',
            'style':"margin-top: 30%;height: 35%;width: 100%;"       
            
        })
    )

    price = django_filters.ModelMultipleChoiceFilter(
        queryset = Product.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs={
            'class':'form-check-label',
            'style':"margin-top: 30%;height: 35%;width: 100%;"
        })
    )

    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte', widget=forms.NumberInput(
        attrs={
            'class':"form-control",
            'placeholder':'$GTE',
            'style':"font-size: 16px;color: hsl(0, 0%, 10%);border: 2px solid hsl(0, 0%, 90%);background-color: hsl(0, 0%, 100%);font-size: 12px;border-width: 1px;border-radius: 2px;padding: 8px;padding-left: 16px;width: 100px;height: 32px;"
        }
    ))
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte', widget=forms.NumberInput(
        attrs={
            'class':"form-control",
            'placeholder':'$LTE',
            'style':"font-size: 16px;color: hsl(0, 0%, 10%);border: 2px solid hsl(0, 0%, 90%);background-color: hsl(0, 0%, 100%);font-size: 12px;border-width: 1px;border-radius: 2px;padding: 8px;padding-left: 16px;width: 100px;height: 32px;"
        }
    ))

    class Meta:
        model = Product
        fields = [
            'title',
            'catagory',
            'brand',
            'color',
            'min_price',
            'max_price',
        ]