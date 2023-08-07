from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from cloudinary.models import CloudinaryField
import secrets
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

#Common Fields for every table

class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=False,null=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False,null=False)

    class Meta:
        abstract = True


# User table 


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    password = models.CharField(max_length=100, null=False, blank=True)
    email = models.EmailField(unique=True, blank=True)
    address = models.TextField(max_length=250, blank=True)
    jwt_token = models.CharField(max_length=250, unique=True, null=True, blank=True)
    token = models.CharField(max_length=250, unique=True, null=True, blank=True)
    is_logged_in = models.BooleanField(default=False)
    display_picture = CloudinaryField('Display Picture', null=True, blank=True)
    objects = UserManager()

    # Use 'phone_number' as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number']

    class Meta:
        db_table = 'User'

    def save_token(self, *args, **kwargs):
        if not self.token:
            # generate new token if none exists
            self.token = secrets.token_urlsafe(32)

        super().save(*args, **kwargs)

    def update_token(self):
        self.token = None
        self.token_created = None
        self.token_expires = None
        self.save()

########### Category Table ##############


class Category(models.Model):
    class Meta:
        db_table = 'Category'
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


################ Item Model ###################


class Size(models.Model):
    class Meta:
        db_table = 'Cloth sizes'
    sizes = models.CharField('Item size',max_length=5,blank=False,null=False)

    def __str__(self):
        return self.sizes

class Items(models.Model):
    class Meta:
        db_table = 'Item'
    
    item_name = models.CharField(max_length=50,blank=False,null=False)
    item_price = models.FloatField(blank=False,null=False)
    size = models.ManyToManyField(Size,blank=False)
    item_image = CloudinaryField("Item Image",blank=False,null=False)
    is_available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    inventory = models.IntegerField(default=0)

    def __str__(self):
        return self.item_name
    
##################### Cart Model ####################


class Cart(models.Model):
    class Meta:
        db_table = 'Cart'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Items', through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}" 
    

class CartItem(models.Model):
    class Meta:
        db_table = 'Cart_Items'
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey('Items', on_delete=models.CASCADE)
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # New field for quantity
    
    def __str__(self):
        return f"{self.cart} - {self.item.item_name} ({self.size.sizes}) - Quantity: {self.quantity}"
    @property
    def total_price(self):
        return self.item.item_price * self.quantity


############ order model ####################


class Order(models.Model):
    PAYMENT_CHOICES = (
        ("CASH ON DELIVERY", "COD"),
        ("UPI", "UPI"),
        ("CARD", "CARD"),
    )
    TRACKING = (
        ('SHIPPED','shipped'),
        ('ON THE WAY','on the way'),
        ('DELIVERED','delivered')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    zip_code = models.CharField(max_length=10)
    place = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    tracking = models.CharField(max_length=20,choices=TRACKING,blank=True,null=True)
    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey('apps.Items', on_delete=models.CASCADE)
    size = models.ForeignKey('apps.Size', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    total_price = models.IntegerField(null=False, blank=False)
    def __str__(self):
        return f"{self.order} - {self.item.item_name} ({self.size.sizes})"
    

############# Wishlist ################


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist: {self.item.name}"
    


################# subscriber model ##############################


class Subscriber(models.Model):
    name = models.CharField(max_length=100,blank=False,null=False)
    email = models.EmailField(unique=True, blank=True)

