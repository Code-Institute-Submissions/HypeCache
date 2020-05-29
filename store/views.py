from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from hypecache.settings import STRIPE_SECRET
from .models import *
import json
import stripe
stripe.api_key=STRIPE_SECRET

# Create your views here.
# ? HOME View
class ProductListView(ListView):
    model = Product
    template_name = "store/home.html"
    context_object_name='products'
    ordering = ['-date_posted']

# ? CART View
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
    order = Order.objects.get(customer=customer)
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

    session = stripe.checkout.Session.create(
        customer_email=customer.email,
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
def success(request):
    return render(request,'store/success.html')

# ? ADD SHIPPING ADDRESS
# If not address found:
class ShippingCreateView(CreateView):
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
class ProductCreateView(CreateView):
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
    elif action=='cart_input':
        orderItem.quantity = (orderItem.quantity- value )
    # elif action=='delete':
    #     orderItem.delete()

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)