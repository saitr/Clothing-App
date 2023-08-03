from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.forms import OrderForm
from apps.models import Cart, CartItem, Order, OrderItem
from decimal import Decimal


@login_required
def place_order(request):
    user_cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=user_cart)

    total_cart_value = Decimal(0)
    for cart_item in cart_items:
        item_price = Decimal(str(cart_item.item.item_price))  # Convert float to Decimal
        total_cart_value += item_price * Decimal(cart_item.quantity)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Create order items for each item in the cart
            cart_items = CartItem.objects.filter(cart=user_cart)
            for cart_item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    size=cart_item.size,
                    quantity=cart_item.quantity,
                    total_price=cart_item.item.item_price * cart_item.quantity,  # Calculate total_price
                )
            
            # Empty the cart
            user_cart.items.clear()

            return redirect('order_confirmation')  # Redirect to a confirmation page after successful order placement

    else:
        form = OrderForm()
        cart_items = CartItem.objects.filter(cart=user_cart)  # Fetch cart items for the logged-in user

    return render(request, 'order_form.html', {'form': form, 'cart_items': cart_items,'total_cart_value': total_cart_value})

@login_required
def order_confirmation(request):
    # You can implement a confirmation page here if you want to show order details
    return render(request, 'order_confirmation.html')  