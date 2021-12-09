from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views.generic import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.
import random
import string
import stripe
stripe.api_key = "sk_test_51HEtKGL8BxQy57KfDDoOgx9HkwDZXH16fTSh5q0pty24ndg9o3RBdfvQFVNKHOgPHhhRq2pieS8aw7gGWBgObMQI00EuUjNyUc"


def index(request):
    carousels = Carousel.objects.all().order_by('-id')

    categorise = Category.objects.all().order_by('id')[:4]
    categorise_step_2 = Category.objects.all().order_by('id')[5:9]
    
    product = Product.objects.all()
    today_deals_product = Product.objects.all()
    Top_Beauty_and_Personal_Care_Product = Product.objects.all()

    today_deals_all_link = Category.objects.all().order_by('id')[4:5]
    Top_Beauty_and_Personal_Care_Product_all_link = Category.objects.all().order_by('id')[9:10]


    context ={
        'carousels':carousels,

        'categorise': categorise,
        'categorise_step_2':categorise_step_2,

        'product':product,
        'Top_Beauty_and_Personal_Care_Product':Top_Beauty_and_Personal_Care_Product,
        'today_deals_product':today_deals_product,

        'today_deals_all_link':today_deals_all_link,
        'Top_Beauty_and_Personal_Care_Product_all_link':Top_Beauty_and_Personal_Care_Product_all_link,


    }
    return render(request, 'index.html', context)


def product_category(request, name):
    cate = get_object_or_404(Category, category_name=name)
    product =Product.objects.filter(product_category=cate.id)

    context={
        'cate':cate,
        'product':product
    }
    return render(request,'product_category.html', context)

def product_details(request,slug):
    details =Product.objects.get(slug=slug)
    related_product =Product.objects.filter(product_category=details.product_category).exclude(slug=slug)[:4] 

    context={
        'details':details,
        'related_product':related_product
    }
    return render(request, 'product_detail.html',context)\

def ProductSearch(request):
    query=request.GET['q']
    lookups =Q(title__icontains=query) | Q(price__icontains=query) 
    data = Product.objects.filter(lookups).order_by('-id')

    context ={
        'data':data
    }
    return render(request, 'search.html',context)

# class ProductDetailsView(DetailView):
#     model = Product
#     template_name ='product_detail.html'
@login_required
def add_to_cart(request, slug): 
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        #check the order product in the order 
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, 'This Product quantity has been updated')
            return redirect('product-detail', slug=slug)

        else:
            order.products.add(order_product)
            messages.info(request, 'This Product has been added to cart')
            return redirect('product-detail', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, 'This Product has been added to cart')
        return redirect('product-detail', slug=slug)
    return redirect('product-detail', slug=slug)        

@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        #check the order product in the order 
        if order.products.filter(product__slug=product.slug).exists():
            order_product.delete()
            messages.info(request, 'This product  has been delete')
            return redirect('product-detail', slug=slug)

        else:
            messages.info(request, 'This product was not your cart')
            return redirect('product-detail', slug=slug)
    else:
        messages.info(request, 'This product was not cart')
        return redirect('product-detail', slug=slug)
    return redirect('product-detail', slug=slug)

class CartSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            context={
                 'order':order
            }
            return render(self.request, 'cart_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, " Your cart is empty")
            return redirect('/')
@login_required
def cart_product_increment(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        #check the order product in the order 
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, 'This Product quantity has been updated')
            return redirect('cart-summary')

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, 'This Product has been added to cart')
        return redirect('cart-summary')
    return redirect('cart-summary') 


@login_required
def cart_product_decrement(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        #check the order product in the order 
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity -= 1
            order_product.save()
            messages.info(request, 'This Product quantity has been updated')
            return redirect('cart-summary')
        else:
            order_product.delete()
            messages.info(request, 'This Product was deleted')
            return redirect('cart-summary')

    else:
        return redirect('cart-summary')
    return redirect('cart-summary')  

@login_required
def cart_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        #check the order product in the order 
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(user=request.user, ordered=False)[0]
            order_product.delete()
            messages.info(request, 'This Product  has been delete')
            return redirect('cart-summary')
        else:
            messages.info(request, 'This Product was not your cart')
            return redirect('cart-summary')

    else:
        messages.info(request, 'This Product was not your cart')
        return redirect('cart-summary')
    return redirect('cart-summary')  


class CustomerOrderStatusView(View):
    def get(self, *args, **kwargs):
        try:
            order =OrderProduct.objects.filter(user=self.request.user)           
            context={
                'order':order
            }
            return render(self.request, 'customerorderstatus.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request, " Your ordre is empty")
            return redirect('/')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            form=CheckoutForm()
            order = Order.objects.get(user=self.request.user, ordered=False)
            context={
                'form':form,
                'order':order
            }
            return render(self.request, 'checkout.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order')
            return redirect('checkout')
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                present_address = form.cleaned_data.get('present_address')
                home_address = form.cleaned_data.get('home_address')
                mobile_number = form.cleaned_data.get('mobile_number')
                payment_option = form.cleaned_data.get('payment_option')
                checkout=Checkout(
                    user = self.request.user,
                    present_address = present_address,
                    home_address=home_address,
                    mobile_number=mobile_number
                )
                checkout.save()
                order.save()
                # TODO: and rediirect to the selected payment option
                if payment_option == 'S':
                    return redirect('payment', payment_option='stripe')
                elif payment_option == 'B':
                    return redirect('payment', payment_option='bkash')
                else:
                    return redirect('checkout')
                    messages.warning(self.request, "Checkout Failed")
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('checkout')

class PaymentView(View):
    def get(self,*args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)

        context={
            'order':order
        }
        return render(self.request, 'payment.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount= int(order.get_total() * 100)


        try:
            charge = stripe.Charge.create(
                amount= amount,
                currency="usd",
                source= token,
            )
            #create the payment
            payment = Payment()
            payment.stripe_charge_id =charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            #assing the payment to the order
            order_products = order.products.all()
            order_products.update(ordered=True)
            for product in order_products:
                product.save()

            order.ordered =True
            order.payment = payment
            order.save()
            # TODO assign ref code
            messages.success(self.request, "You order was successful")
            return redirect('/') 

                                
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('messages')}")
            return redirect('/')
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit erro")
            return redirect('/') 

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "invalid parameters")
            return redirect('/')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Not Authenticated")
            return redirect('/')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network error")
            return redirect('/')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something is wrong")
            return redirect('/')
        except Exception as e:
            # Send an email to ourselves
            messages.error(self.request, "Serious erro")
            return redirect('/')

