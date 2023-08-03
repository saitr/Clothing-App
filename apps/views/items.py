from django.shortcuts import render, get_object_or_404, redirect
from apps.models import Items, Wishlist, Category, Subscriber
from django.contrib.auth.decorators import login_required
from apps.forms import ItemForm
from django.http import JsonResponse

def item_list(request):
    categories = Category.objects.all()
    items = Items.objects.all()
    return render(request, 'item_list.html', {'items': items, 'categories': categories})

def item_detail(request, item_id):
    item = get_object_or_404(Items, pk=item_id)
    print('this is item_detail',item.id)
    return render(request, 'item_detail.html', {'item': item})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            return redirect('item_detail', item_id=item.pk)
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})

def edit_item(request, item_id):
    item = get_object_or_404(Items, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect('item_detail', item_id=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form})

def delete_item(request, item_id):
    item = get_object_or_404(Items, pk=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'confirm_delete_item.html', {'item': item})


#### about page rendering #########


def about(request):
    return render(request, 'about.html')



######################### Wishlist Functionality #######################


@login_required
def add_to_wishlist(request, item_id):
    item = Items.objects.get(pk=item_id)
    Wishlist.objects.get_or_create(user=request.user, item=item)
    return redirect('item_list')

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def remove_from_wishlist(request, wishlist_item_id):
    try:
        wishlist_item = Wishlist.objects.get(pk=wishlist_item_id, user=request.user)
        wishlist_item.delete()
    except Wishlist.DoesNotExist:
        # Handle case when the wishlist item doesn't exist
        pass
    return redirect('view_wishlist')



########### Filter items by the Categorys #####################


def filter_items_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    items = Items.objects.filter(category=category)
    return render(request, 'filter.html', {'items': items, 'category': category})



####################### Contact page #######################


def contact(request):
    return render(request, 'contact.html')



##################### subscribing ######################

def subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        if Subscriber.objects.filter(email=email).exists():
            message = 'Email already subscribed.'
            success = False
        else:
            Subscriber.objects.create(name=name, email=email)
            message = 'Successfully subscribed to the newsletter.'
            success = True

        return JsonResponse({'message': message, 'success': success})
    else:
        return render(request, 'subscribe.html')