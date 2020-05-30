from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from hypecache.settings import STRIPE_SECRET,ENDPOINT_SECRET
from .models import *
import json
import stripe
stripe.api_key=STRIPE_SECRET
endpoint_secret =ENDPOINT_SECRET

# Create your views here.
# ? HOME View
class ProductListView(ListView):
    model = Product
    template_name = "store/home.html"
    context_object_name='products'
    ordering = ['-date_posted']
    paginate_by=6

# ? CART View
# !remove auth user logic
@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created=Order.objects.get_or_create(customer=customer, confirmed=False)
        items = order.orderitem_set.all()
        try:
            address = ShippingAddress.objects.get(customer=customer)
        except:
            address=None
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}

        

    context={'items':items,'order':order,'address':address}
    return render(request,'store/cart.html',context)

#  ? CHECKOUT
# Create checkout session
def build_checkout_session(customer):
    order = Order.objects.get(customer=customer,confirmed=False)
    customer_email=customer.email
    customer_stripe=customer.stripe_id
    items = order.orderitem_set.all()
    prices =[]
    for item in items:
        product =stripe.Product.create(
            name = item.product.name,
            description= item.product.description
        )
        price = stripe.Price.create(
            product= product.id,
            unit_amount=int(item.product.price.amount)*100,
            currency='gbp',
        )
        prices.append(price.id)

    line_items=[]
    for item, price in zip(items,prices):
            line_items.append({'price':price,'quantity':item.quantity}),

    if customer_stripe:
        customer_email=None


    session = stripe.checkout.Session.create(
        customer_email=customer_email,
        customer=customer_stripe,
        payment_method_types=['card'],
        line_items=line_items,
        
        mode='payment',
        success_url='http://127.0.0.1:8000/SUCCESS/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/cart'
        )
    return session

# Load Stripe Checkout
def checkout(request):
    session = build_checkout_session(customer = request.user.customer)
    return render(request, 'store/checkout.html', {'session_id': session.id})

# SUCCESS PAGE AFTER PAYMENT
@login_required
def success(request):
    return render(request,'store/success.html')

# ? ADD SHIPPING ADDRESS
# If not address found:

class ShippingCreateView(LoginRequiredMixin,CreateView):
    model = ShippingAddress
    template_name = "store/shipping.html"
    fields=[
        'first_name',
        'last_name',
        'address',
        'city',
        'postcode'
    ]
    def form_valid(self,form):
        form.instance.customer=self.request.user.customer
        form.instance.order=Order.objects.get(customer=self.request.user.customer)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('checkout')

# If user has address set:

class ShippingUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = ShippingAddress
    template_name = "store/shipping.html"
    fields=[
        'first_name',
        'last_name',
        'address',
        'city',
        'postcode'
    ]
    def test_func(self):
        address=self.get_object()
        if get_object_or_404(Customer,user=self.request.user) == address.customer:
            return True
        else:
            return False
    def get_success_url(self):
        return reverse('checkout')


# ? Filter Products by Category
class FilterListView(ListView): 
    model = Product 
    template_name = "store/home.html" 
    context_object_name='products' 
    ordering = ['-date_posted']

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs.get('category'))


# ? Individual Post View
class ProductDetailView(DetailView):
    model = Product


#? Create Store Post for staff only
class ProductCreateView(UserPassesTestMixin , CreateView):
    model = Product
    fields=[
        'name',
        'image',
        'condition',
        'brand',
        'category',
        'description',
        'size',
        'colour',
        'price',
        'in_stock',
        'for_sale'
    ]
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False

    #? Update Posts
class ProductUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
    ):
    model = Product
    fields=[
        'name',
        'image',
        'condition',
        'brand',
        'category',
        'description',
        'size',
        'colour',
        'price',
        'in_stock',
        'for_sale'
    ]
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            return False

# ? Delete Post View
class ProductDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
    ):
    model = Product
    success_url='/'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

@login_required
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action=data['action']
    print('Action:',action)
    print('Product:',productId)

    customer = request.user.customer
    product= Product.objects.get(id=productId)
    order, created=Order.objects.get_or_create(customer=customer,confirmed=False)

    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action=='remove':
        orderItem.quantity = (orderItem.quantity -1) 
    elif action=='delete':
        orderItem.quantity = (orderItem.quantity -orderItem.quantity) 


    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

# ? WEBHOOK
@require_http_methods(["POST"])
@csrf_exempt
def receive_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
        json.loads(payload), stripe.api_key
        )
    except ValueError as e:
    # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'charge.succeeded':
        stripe_charge = event.data.object 
        cust_email=stripe_charge.billing_details.email
        cust_id = stripe_charge.customer
        receipt_url=stripe_charge.receipt_url
        customer = Customer.objects.get(email=cust_email)
        order=Order.objects.get(customer=customer, confirmed=False)
        order.confirmed = True
        order.transaction_id=stripe_charge.payment_intent
        order.save()
        if not customer.stripe_id:
            customer.stripe_id = cust_id
        
        customer.save()
        # send_mail(
        #     'HypeCache - Thank you for your order!',
        #     receipt_url,
        #     'donotreply@hypecache.com',
        #     [cust_email],
        #     fail_silently=False,
        # )

    else:
    # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)