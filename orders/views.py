from django.shortcuts import render
from .models import OrderItem,Order
from cart.cart import Cart
from .forms import OrderCreateForm
from .tasks import order_created
from django.core.mail import send_mail
from django.conf import settings
import stripe 

stripe.api_key = settings.STRIPE_SECRET_KEY 

# Create your views here.

def order_create(request):
    cart = Cart(request)
    amount = int(cart.get_total_price()) 
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
            
            charge = stripe.Charge.create(
                amount=amount * 100,
                currency='usd',
                description='A Django charge',
                source=request.POST['stripeToken'])

            order1 = Order.objects.all()
            order1.paid = True
            context = {
                'order':order,
                'charge':charge,
            }
            return render(request, 'orders/order_success.html',context)

    else:
        form = OrderCreateForm()
    key = settings.STRIPE_PUBLISHABLE_KEY
    context = {
        'form':form,
        'cart':cart,
        'key':key,
    }
    return render(request, 'orders/checkout.html', context)