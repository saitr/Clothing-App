from django.urls import path
from apps.views.users import *
from apps.rest_api.user import *
from apps.views.items import * 
from apps.views.carts import *
from apps.views.orders import *


urlpatterns = [
    # Normal django urls

    # User urls
    path('signup/',signup,name='signup'),
    path('verify/<str:email>/',verify,name='verify'),
    path('logout/',logout_user,name='logout'),
    path('signin/',signin,name='signin'),
    path('user_details/',user_details,name='user_details'),
    # Add the following URL patterns
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<str:email_b64>/', reset_password, name='reset_password'),
    # item Urls
    path('', item_list, name='item_list'),
    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('item/add/', add_item, name='add_item'),
    path('item/edit/<int:item_id>/', edit_item, name='edit_item'),
    path('item/delete/<int:item_id>/', delete_item, name='delete_item'),
    path('about/', about, name='about'),
    path('item_list/<int:category_id>/', filter_items_by_category, name='filter_items_by_category'),
    path('contact/',contact,name='contact'),
    path('subscribe',subscribe,name='subscribe'),
    ###### Wishlist urls ############

    path('add_to_wishlist/<int:item_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('view_wishlist/', view_wishlist, name='view_wishlist'),
    path('wishlist/remove/<int:wishlist_item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    # Cart urls 

    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='cart'),
    path('update_quantity/<int:cart_item_id>/', update_quantity, name='update_quantity'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),

    # Order urls 

    path('place_order/', place_order, name='place_order'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),
    path('orders/', order_list, name='order_list'),
    path('orders/<int:order_id>/update_tracking/', update_tracking, name='update_tracking'),

    # rest api endpoints 
    path('rest_signup/',SignUpView.as_view(), name='rest_signup'),
    path('rest_signin/',SigninView.as_view(),name='rest_signin'),
    path('rest_logout/',LogoutView.as_view(), name='rest_logout'),
    path('rest_verify/<str:email>/',VerifyOtpView.as_view(), name='VerifyRestEmail'),
]