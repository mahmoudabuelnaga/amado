from django.shortcuts import render
from .models import OrderItem
from cart.cart import Cart
from .forms import OrderCreateForm
from .tasks import order_created
from django.core.mail import send_mail


# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            context = {
                'order':order,
            }
            return render(request, 'orders/order_success.html',context)
    
    else:
        form = OrderCreateForm()
    context = {
        'form':form,
        'cart':cart,
    }
    return render(request, 'orders/checkout.html', context)