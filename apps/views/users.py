from django.conf import settings
from django.contrib.auth import login
from django.core.mail import send_mail,EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
# form imports 
from apps.forms import SignUpForm,VerifyOTPForm,SignInForm,ChangeUserDetails
from django.http import HttpResponse
from apps.models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.authtoken.models import Token
import secrets
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
##checks for login
from django.contrib.auth.decorators import login_required
import concurrent.futures
import phonenumbers
from django.core.mail import send_mail

def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

def send_mail_async(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            country_code = form.cleaned_data.get('country_code')
            phone_number = form.cleaned_data.get('phone_number')
            
            # Add the country code to the phone number
            full_phone_number =  phone_number
            print(full_phone_number)
            if User.objects.filter(email=email, username=username).exists():
                form.add_error('email', 'Email already exists')
                return render(request, 'signup_sai.html', {'form': form})

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
                return render(request, 'signup_sai.html', {'form': form})

            if not validate_phone_number(full_phone_number):
                form.add_error('phone_number', 'Invalid phone number')
                return render(request, 'signup_sai.html', {'form': form})
            # generate OTP and save it to user model
            otp = get_random_string(length=6, allowed_chars='1234567890')
            user = User.objects.create_user(
                username=form.cleaned_data.get('username'),
                email=email,
                phone_number=form.cleaned_data.get('phone_number'),
                address=form.cleaned_data.get('address'),
                otp=otp,
                password=form.cleaned_data.get('password')
            )

            # to create a token
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token(user=user)

            token.key = secrets.token_urlsafe(32)
            token.created = timezone.now()
            token.expires = token.created + timedelta(days=7)
            token.save()

            # Send email with OTP asynchronously
            subject = 'Verify your email'
            message = f'Your OTP is {otp}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            # Use concurrent.futures to send the email in a separate thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(send_mail_async, subject, message, from_email, recipient_list)
            # Redirect to verify page
            return redirect('verify', email=email)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})





############################## to verify the email while signing up##################################

def verify(request, email):
    user = User.objects.get(email=email)

    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            if otp == user.otp:
                user.is_active = True
                user.is_verified = True
                user.is_logged_in = True
                user.save()

                # Send thank you email
                subject =  'Welcome To The Family'
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [email]

                html_content = render_to_string('thankyouemail.html')
                text_content = strip_tags(html_content)

                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, 'text/html')
                msg.send()

                # Authenticate and log in the user
                
                login(request,user)
                user.save_token()

                
                if login:
                    print('successfully logged in')
                else:
                    print('failed to login')

                if request.user.is_authenticated:
                    print("Logged in")
                else:
                    print("Not logged in")
                return redirect('item_list')
            else:
                form.add_error('otp', 'Invalid OTP. Please try again.')
    else:
        form = VerifyOTPForm()

    return render(request, 'verify.html', {'form': form})

#######################################logout view#######################################



def logout_user(request):
    if request.user.is_authenticated:
        user = request.user
        user.token = None
        print('thisi sit',user.token)
        user.is_logged_in = False
        user.save()
        logout(request)
    return redirect('signin')




########################################### signin view###################################


# def signin(request):
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             username= form.cleaned_data['username']
#             print('login username',username)
#             password= form.cleaned_data['password']
#             print('login password',password)
            
#             user = User.objects.get(username=username,password=password)
#             if user:
#                 login_user = user

#                 login(request,login_user)
#                 try:
#                     token = Token.objects.get(user=user)
#                 except Token.DoesNotExist:
#                     token = Token(user=user)
                
#                 token.key = secrets.token_urlsafe(32)
#                 token.created = timezone.now()
#                 token.expires = token.created + timedelta(days=7)
#                 token.save()

#                 if login:
#                     print('login successful')
#                 else:
#                     print('login failed')
#                 user.is_logged_in = True
#                 user.save()
#                 return redirect('home')
#             else:
#                 form.add_error('no correct username or password')
   
#     else:
#         form = SignInForm()
#     return render(request, 'signin.html', {'form': form})



from django.contrib.auth.hashers import check_password

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if the input is a valid phone number
            if validate_phone_number(username):
                # If it's a valid phone number, authenticate using phone number
                try:
                    user = User.objects.get(phone_number=username)
                except User.DoesNotExist:
                    form.add_error('username_or_phone', 'Incorrect username or password')
                    return render(request, 'signin.html', {'form': form})
            else:
                # If it's not a valid phone number, authenticate using username
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    form.add_error('username', 'Incorrect username or password')
                    return render(request, 'signin.html', {'form': form})

            # Use check_password to validate the password
            if not check_password(password, user.password):
                form.add_error('username', 'Incorrect username or password')
                return render(request, 'signin.html', {'form': form})

            login(request, user)

            # Delete any existing tokens for the user
            user.save_token()

            user.is_logged_in = True
            user.save()

            return redirect('item_list')

    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})



############################ user details ##################################

# @login_required
# def user_details(request):
#     user = request.user

#     if request.method == 'POST':
#         form = ChangeUserDetails(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             phone_number = form.cleaned_data['phone_number']
#             address = form.cleaned_data['address']

#             request.user.username = username
#             request.user.email = email
#             request.user.phone_number = phone_number
#             request.user.address = address

#             user.save()
#             return redirect('home')
#     else: 
#         form = ChangeUserDetails()
#     # user = request.user
#     # context = {'user': user}
#     return render(request, 'user_details.html',{'form':form})


@login_required(login_url='signin')
def user_details(request):
    user = request.user
    users = User.objects.all()
    if request.method == 'POST':
        form = ChangeUserDetails(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            display_picture = form.cleaned_data['display_picture']

            request.user.username = username
            request.user.email = email
            request.user.phone_number = phone_number
            request.user.address = address
            
            # Save display picture if provided
            if display_picture:
                user.display_picture = display_picture
                
            request.user.save()
            return redirect('item_list')
    else:
        initial_data = {
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'address': user.address,
        }
        form = ChangeUserDetails(initial=initial_data)
    
    return render(request, 'user_details.html', {'form': form,'users': users})






# from django.core.mail import send_mail
# from django.contrib import messages

# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email', '')

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             user = None

#         if user:
#             # Encode the email as Base64
#             email_b64 = urlsafe_base64_encode(force_bytes(email))

#             # Create the reset URL
#             reset_url = f"{request.build_absolute_uri('/reset_password/')}{email_b64}/"

#             # Compose the email content
#             subject = 'Password Reset'
#             message = f'Click the following link to reset your password: {reset_url}'
#             from_email = settings.DEFAULT_FROM_EMAIL
#             recipient_list = [email]

#             # Send the email
#             send_mail(subject, message, from_email, recipient_list)

#             messages.success(request, 'A reset link has been sent to your email.')
#             return redirect('forgot_password')

#         else:
#             messages.error(request, 'No user found with this email.')
#             return redirect('forgot_password')

#     return render(request, 'forgot_password.html')

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            # Encode the email as Base64
            email_b64 = urlsafe_base64_encode(force_bytes(email))

            # Create the reset URL using the DOMAIN_NAME from settings
            reset_url = f"{settings.DOMAIN_NAME}reset_password/{email_b64}/"

            # Compose the email content
            subject = 'Password Reset'
            message = f'Click the following link to reset your password: {reset_url}'

            # Send the email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            messages.success(request, 'A reset link has been sent to your email.')
            return redirect('forgot_password')

        else:
            messages.error(request, 'No user found with this email.')
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')


from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str  # Use force_str instead of force_text

def reset_password(request, email_b64):
    email = force_str(urlsafe_base64_decode(email_b64))  # Use force_str instead of force_text

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None

    if user:
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()

            messages.success(request, 'Password reset successfully. You can now login with the new password.')
            return redirect('signin')

        return render(request, 'reset_password.html', {'email_b64': email_b64})
    else:
        messages.error(request, 'Invalid reset link.')
        return redirect('signin') 

