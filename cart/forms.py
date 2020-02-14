from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity    = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class':"qty-text",
        'id':"qty",
        'step':"1",
        'min':"1",
        'max':"300",
        'value':'1',
    }))
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update      = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput) 