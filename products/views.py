from django.shortcuts import render, get_object_or_404
from .models import (Catagory,Image,Color,Brand,Product,)
from django.views.generic import ListView , DetailView
import datetime
from .filters import ProductFilter
from django.db.models import Max, Min
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.forms import CartAddProductForm

# Create your views here.
class Home(ListView):
    model = Catagory
    template_name = 'product/index.html'

    def Query_set(self):
        return Product.objects.filter(catagory=Catagory)
    

class CatagoryDetailView(DetailView):
    model = Catagory
    template_name = 'product/catagory-detail.html'
    context_object_name = 'obj'


# class ProductListView(ListView):
#     model = Product
#     template_name = 'product/shop.html'

#     def Query_set(self):
#         return ProductFilter(self.request.GET, queryset=Product)

#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductListView, self).get_context_data(*args, **kwargs)
#         context['object_list'] = Product.objects.all()
#         context['filter'] = ProductFilter(self.request.GET, queryset=self.object_list)
#         return context

def product_list_view(request):
    cart_product_form = CartAddProductForm()
    products = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products)
    # product_filter_qs = ProductFilter(request.GET, queryset=products).qs

    # paginator
    paginator = Paginator(product_filter.qs, 20)
    page = request.GET.get('page')

    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    context = {
        'filter':product_filter,
        'product':product,
        'cart_product_form':cart_product_form,
    }
    return render(request, 'product/shop.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product-detail.html'
    context_object_name = 'obj'

    def Query_set(self):
        return Image.objects.filter(product=Product)   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm()
        return context
     