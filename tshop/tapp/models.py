from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Carousel(models.Model):
    title = models.CharField(max_length=100)
    caro_img = models.ImageField( upload_to= 'CaroImg' )

    def __str__(self):
        return self.title

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_img = models.ImageField(upload_to='Category_Img')

    def __str__(self):
        return self.category_name

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(upload_to='Product_Img')
    image2 = models.ImageField(upload_to='Product_Img', blank=True, null=True)
    image3 = models.ImageField(upload_to='Product_Img', blank=True,null= True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    date =models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
        
    class Meta:
        ordering =['-date']

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={
            'slug':self.slug
        })

    def get_remove_from_cart(self):
        return reverse('remove-from-cart', kwargs={
            'slug':self.slug
        })
    def get_cart_delete(self):
        return reverse('cart-delete' , kwargs={
            'slug': self.slug
        })
ORDER_STATUS=(
    ('Pending','Pending'),
    ('Processing', 'Processing')
)

class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_status =models.CharField(max_length=100, choices=ORDER_STATUS, default='Pending')

    def __str__(self):
            return f"{self.quantity} of { self.product.title}"

    def get_subtotal(self):
        return self.quantity * self.product.price

    def get_discount_price(self):
        return self.quantity * self.product.discount_price

    def get_saving_price(self):
        return self.get_subtotal() - self.get_discount_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_discount_price()
        return self.get_subtotal()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date =models.DateTimeField(auto_now_add=timezone.now)
    ordered_date = models.DateTimeField(auto_now_add=timezone.now)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for i in self.products.all():
            total += i.get_final_price()
        return total

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    present_address = models.CharField(max_length=200)
    home_address = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=13)
    default =models.BooleanField(default=False)

    def __str__(self):
        return self.user.username 

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True )
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
