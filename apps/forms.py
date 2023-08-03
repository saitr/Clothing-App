from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from apps.models import *
#######################Sign UP form##################################

import phonenumbers

def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False
    

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'UserName'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input--style-2','placeholder': 'Password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input--style-2','placeholder': 'Email'}))
    country_code = forms.ChoiceField(choices=[('+91', '+91 - India'),('+92', '+92 - Pakistan')], widget=forms.Select(attrs={'class': 'input--style-2'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2','placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2','placeholder': 'Address'}))

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'country_code', 'phone_number', 'address')

    def clean_phone_number(self):
        country_code = self.cleaned_data.get('country_code')
        phone_number = self.cleaned_data.get('phone_number')
        full_phone_number = ''

        if country_code and phone_number:
            full_phone_number = country_code + phone_number

        if not validate_phone_number(full_phone_number):
            raise forms.ValidationError('Invalid phone number')

        return full_phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
################# verifying the otp form #########################


class VerifyOTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


###################Signin form#################################

class SignInForm(forms.Form):
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'UserName'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input--style-2','placeholder': 'Password'}))
    class Meta:
        model = User
        fields = ('username', 'password')




################## changing the user_details form #####################

class ChangeUserDetails(forms.Form):
    # username = forms.CharField(max_length=100,label='Username:')
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'UserName'}))
    # email = forms.EmailField(label='Email:')
    email= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input--style-2', 'placeholder': 'Email'}))
    # phone_number = forms.IntegerField(label="Phone Number:")
    phone_number= forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input--style-2', 'placeholder': 'Phone Number'}))
    # address = forms.CharField(max_length=100,label = 'Address:')
    display_picture = forms.FileField(label='Change Display Picture',required=False)


####### This is the class to create an item ########

class ItemForm(forms.ModelForm):
    size = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    item_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Item Name'}))
    item_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'input--style-2', 'placeholder': 'Item Price'}))
    item_image = forms.FileField(label='Change Display Picture', required=False)
    category = forms.ModelChoiceField(queryset=None, empty_label="Select a category")

    class Meta:
        model = Items
        fields = ['item_name', 'item_price', 'size', 'item_image', 'is_available', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].queryset = Size.objects.all()
        self.fields['category'].queryset = Category.objects.all()



############ Order form ##############




class OrderForm(forms.ModelForm):
    PAYMENT_CHOICES = (
        ("CASH ON DELIVERY", "COD"),
        ("UPI", "UPI"),
        ("CARD", "CARD"),
    )

    class Meta:
        model = Order
        fields = ['name', 'phone_number', 'zip_code', 'place', 'payment_method']

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Enter Your Name'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Enter Your Phone Number'}))
    zip_code = forms.CharField(widget=forms.NumberInput(attrs={'class': 'input--style-2', 'placeholder': 'Enter The Zip Code'}))
    place = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Enter The Address'}))
    payment_method = forms.ChoiceField(label='Payment Method', choices=PAYMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'required': True}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) # Get the user object from kwargs
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['address'].initial = self.user.address # Set the default value of the address field to the user's address
