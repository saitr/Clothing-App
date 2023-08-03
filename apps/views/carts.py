from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.models import *

@login_required
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


from decimal import Decimal

@login_required
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

@login_required
def remove_from_cart(request, cart_item_id):
    if request.user:
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem.objects.get(pk=cart_item_id, cart=user_cart)
        cart_item.delete()
        return redirect('cart')
    else:
        # Handle case for non-authenticated users (e.g., redirect to login page)
        pass


@login_required
def update_quantity(request, cart_item_id):
    if request.method == 'POST':
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem.objects.get(pk=cart_item_id, cart=user_cart)

        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'increment':
                cart_item.quantity += 1
            elif action == 'decrement':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                else:
                    cart_item.delete()  # Delete the cart item if the quantity becomes zero
                    return redirect('cart') # Return here to avoid saving the cart item

            if cart_item.quantity > 0: # Add this condition to check if quantity is greater than 0
                cart_item.save()
            else:
                cart_item.delete()
                return redirect('cart') # Return here to avoid saving the cart item

    return redirect('cart')


