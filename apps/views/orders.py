from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.forms import OrderForm
from apps.models import Cart, CartItem, Order, OrderItem


from django.contrib import messages 
from django.db.models import F
from decimal import Decimal




@login_required
def place_order(request):

    user_cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=user_cart)

    total_cart_value = Decimal(0)
    for cart_item in cart_items:
        item_price = Decimal(cart_item.item.item_price)
        total_cart_value += item_price * cart_item.quantity

    if request.method == 'POST':

        # Validate inventory
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.item.inventory:
                messages.error(request, "Not enough inventory for " + cart_item.item.item_name)
                return redirect("cart")

        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Create order items
            for cart_item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    size=cart_item.size,
                    quantity=cart_item.quantity,
                    total_price=cart_item.item.item_price * cart_item.quantity,
                )

                # Reduce inventory
                cart_item.item.inventory -= cart_item.quantity
                cart_item.item.save()

                # Check if item is available
                if cart_item.item.inventory == 0:
                    cart_item.item.is_available = False
                    cart_item.item.save()

            # Clear user cart
            user_cart.items.clear()

            return redirect('order_confirmation')

    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_cart_value': total_cart_value
    }

    return render(request, 'order_form.html', context)




# @login_required
# def place_order(request):
#     user_cart = Cart.objects.filter(user=request.user).first()
#     cart_items = CartItem.objects.filter(cart=user_cart)

#     total_cart_value = Decimal(0)
#     for cart_item in cart_items:
#         item_price = Decimal(str(cart_item.item.item_price))  # Convert float to Decimal
#         total_cart_value += item_price * Decimal(cart_item.quantity)

#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.save()

#             # Create order items for each item in the cart
#             cart_items = CartItem.objects.filter(cart=user_cart)
#             for cart_item in cart_items:
#                 order_item = OrderItem.objects.create(
#                     order=order,
#                     item=cart_item.item,
#                     size=cart_item.size,
#                     quantity=cart_item.quantity,
#                     total_price=cart_item.item.item_price * cart_item.quantity,  # Calculate total_price
#                 )
            
#             # Empty the cart
#             user_cart.items.clear()

#             return redirect('order_confirmation')  # Redirect to a confirmation page after successful order placement

#     else:
#         form = OrderForm()
#         cart_items = CartItem.objects.filter(cart=user_cart)  # Fetch cart items for the logged-in user

#     return render(request, 'order_form.html', {'form': form, 'cart_items': cart_items,'total_cart_value': total_cart_value})

@login_required
def order_confirmation(request):
    # You can implement a confirmation page here if you want to show order details
    return render(request, 'order_confirmation.html')  



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required
def order_list(request):
    if request.user.is_superuser:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'order_list.html', context)

@login_required
def update_tracking(request, order_id):
    if not request.user.is_superuser:
        return redirect('order_list')

    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        tracking = request.POST.get('tracking')
        if tracking in dict(Order.TRACKING):
            order.tracking = tracking
            order.save()

    return redirect('order_list')
