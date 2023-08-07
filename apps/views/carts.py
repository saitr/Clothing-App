from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.models import *
from django.contrib import messages



@login_required(login_url='signin')
def add_to_cart(request, item_id):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    item = Items.objects.get(pk=item_id)
    selected_size = request.POST.get('selected_size')
    size = Size.objects.get(sizes=selected_size)
    quantity = int(request.POST.get('quantity', 1))  # Assuming you have a form field for quantity

    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, item=item, size=size)
    cart_item.quantity = quantity
    cart_item.save()

    return redirect('cart')



# @login_required
# def add_to_cart(request, item_id):
#     item = Items.objects.get(pk=item_id)

#     # Get the quantity from the request's POST data
#     quantity_str = request.POST.get('quantity')
#     if not quantity_str:
#         messages.error(request, "Please provide a quantity.")
#         return redirect('item_detail', item_id)

#     try:
#         quantity = int(quantity_str)
#     except ValueError:
#         messages.error(request, "Invalid quantity. Please provide a valid number.")
#         return redirect('item_detail', item_id)

#     if quantity <= 0:
#         messages.error(request, "Invalid quantity. Please provide a positive number.")
#         return redirect('item_detail', item_id)

#     if item.inventory < quantity:
#         messages.error(request, "Not enough inventory!")
#         return redirect('item_detail', item_id)

#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

#     cart_item.quantity = quantity
#     cart_item.save()

#     return redirect('cart')

from decimal import Decimal

@login_required(login_url='signin')
def view_cart(request):
    if request.user:
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=user_cart)

        # Calculate total cart value using Decimal
        total_cart_value = Decimal(0)
        for cart_item in cart_items:
            item_price = Decimal(str(cart_item.item.item_price))  # Convert float to Decimal
            total_cart_value += item_price * Decimal(cart_item.quantity)

        return render(request, 'cart.html', {'cart_items': cart_items, 'total_cart_value': total_cart_value})
    else:
        # Handle case for non-authenticated users (e.g., redirect to login page)
        pass

@login_required(login_url='signin')
def remove_from_cart(request, cart_item_id):
    if request.user:
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem.objects.get(pk=cart_item_id, cart=user_cart)
        cart_item.delete()
        return redirect('cart')
    else:
        # Handle case for non-authenticated users (e.g., redirect to login page)
        pass


# @login_required
# def update_quantity(request, cart_item_id):
#     if request.method == 'POST':
#         user_cart, created = Cart.objects.get_or_create(user=request.user)
#         cart_item = CartItem.objects.get(pk=cart_item_id, cart=user_cart)

#         if 'action' in request.POST:
#             action = request.POST['action']
#             if action == 'increment':
#                 cart_item.quantity += 1
#             elif action == 'decrement':
#                 if cart_item.quantity > 1:
#                     cart_item.quantity -= 1
#                 else:
#                     cart_item.delete()  # Delete the cart item if the quantity becomes zero
#                     return redirect('cart')  # Return here to avoid saving the cart item

#             # Save the cart item after updating the quantity


#         # Get the selected size from the POST data
#         selected_size = request.POST.get('selected_size')
#         print(f"Selected Size: {selected_size}")

#         try:
#             # Try to get the Size object with the selected size
#             size = Size.objects.get(sizes=selected_size)
#         except Size.DoesNotExist:
#             # If the Size object doesn't exist, create a new one
#             size = Size.objects.create(sizes=selected_size)

#         # Update the cart item's size
#         cart_item.size = size

#         # Save the cart item after updating the size
#         cart_item.save()

#     return redirect('cart')


@login_required(login_url='signin')
def update_quantity(request, cart_item_id):

  cart_item = CartItem.objects.get(pk=cart_item_id)

  if 'action' in request.POST:
    action = request.POST['action']

    if action == 'increment':
      if cart_item.quantity >= cart_item.item.inventory:
        messages.error(request, "Not enough inventory!")
        return redirect('cart')
      else:
        cart_item.quantity += 1

    elif action == 'decrement':
      if cart_item.quantity > 1:
        cart_item.quantity -= 1  
      else:
        cart_item.delete()
        return redirect('cart')

  # Check inventory after increment/decrement
  if cart_item.quantity > cart_item.item.inventory:
    cart_item.quantity = cart_item.item.inventory

  # Update size  
  selected_size = request.POST.get('selected_size')

  try:
    size = Size.objects.get(sizes=selected_size)
  except Size.DoesNotExist:
    size = Size.objects.create(sizes=selected_size)

  cart_item.size = size
  
  cart_item.save()

  return redirect('cart')


