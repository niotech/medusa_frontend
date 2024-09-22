import json
from django.urls import reverse

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import qrcode
import base64
from io import BytesIO
from web.services.services import (
    create_cart,
    add_to_cart,
    remove_from_cart,
    get_cart_detail,
    get_products,
    browse_all_products,
    get_collections,
    get_collection_name,
    update_shipping_details,
    confirm_order,
    update_cart,
    update_line_item,
    shipping_method,
    create_payment_session,
    select_payment_session,
    get_shipping_options,
    create_customer,
    customer_login,
    check_email_exists,
    login_jwt,
    get_customer_profile,
    change_customer_password,
    my_orders,
    create_payment,
    get_invoice_details,
    get_customer_level,
    get_current_customer,
    get_featured_products
)
from .forms import SignUpForm, SignInForm, NewPasswordForm, ContactForm
from .models import SiteSettings, Page, Contact
from django.contrib import messages
from web.decorators.auth import login_required
from web.utils import generate_random_name  # Import the function

from django.views.generic import DetailView, TemplateView


##
def index_view(request):    
    return render(request, 'page/index.html', {})


### Product list for index
def get_product_list():
    response = browse_all_products()
    if response.status_code == 200:
        products_data = response.json()
        return products_data.get('products', [])
    else:
        return []


##
def product_list_view(request):
    response = browse_all_products()
    ##print('response', response)

    ##print(response.text)  # Print the raw response text for debugging
    if response.status_code == 200:
        products_data = response.json()
        # print(products_data)  # Print the parsed JSON response for debugging
        products = products_data.get('products', [])
        return render(request, 'product/product_list.html', {'products': products})
    else:
        print(f"Failed to load products: {response.status_code}")  # Print the status code if the request failed
        return render(request, 'general/error.html', {'message': 'Failed to load products'})


def product_detail_view(request, product_id):
    response = get_products(product_id=product_id)
    if response.status_code == 200:
        product = response.json().get('product')
        # print(product.get('variants'))
        return render(request, 'product/product_detail.html', {'product': product})
    else:
        return render(request, 'general/error.html', {'message': 'Failed to load product'})


def add_to_cart_view(request, variant_id=None, qty=1):
    if request.method == 'POST':
        # Find the variant_id from the POST data
        variant_id = None
        for key, value in request.POST.items():
            if key.startswith('opt_'):
                variant_id = value
                break

        qty = 1  # Assuming quantity is always 1 for simplicity

    if variant_id is None:
        return render(request, 'general/error.html', {'message': 'No variant selected'})

    cart_id = request.session.get('cart_id')
    if not cart_id:
        # If there is no cart_id in the session, create one
        try:
            region_id = settings.REGION_ID
            cart = create_cart(region_id)
            cart_id = cart['id']
            request.session['cart_id'] = cart_id

        except Exception as e:
            return render(request, 'general/error.html', {'message': f'Failed to create cart: {str(e)}'})

    try:
        # reset qr payment if new
        for method in ['btc', 'usdt', 'xmr']:
            remove_qr_payment(method, request, False)
        add_to_cart(cart_id, variant_id, qty)
        return redirect('cart_detail')
    except Exception as e:
        return render(request, 'general/error.html', {'message': f'Failed to add item to cart: {str(e)}'})


# def add_to_cart_view(request, variant_id, qty):
#     cart_id = request.session.get('cart_id')
#     if not cart_id:
#         # If there is no cart_id in the session, create one
#         try:
#             region_id = settings.REGION_ID
#             cart = create_cart(region_id)
#             cart_id = cart['id']
#             request.session['cart_id'] = cart_id
#         except Exception as e:
#             return render(request, 'general/error.html', {'message': f'Failed to create cart: {str(e)}'})
#
#     try:
#         add_to_cart(cart_id, variant_id, qty)
#         return redirect('cart_detail')
#     except Exception as e:
#         return render(request, 'general/error.html', {'message': f'Failed to add item to cart: {str(e)}'})
#

##

def create_cart_view(request):
    cart_id = request.session.get('cart_id')

    if not cart_id:
        try:
            # region_id = settings.REGION_ID
            cart = create_cart()
            cart_id = cart['id']
            request.session['cart_id'] = cart_id
            return redirect('cart_detail')
        except Exception as e:
            return render(request, 'general/error.html', {'message': f'Failed to create cart: {str(e)}'})

    try:
        cart = get_cart_detail(cart_id)
        return render(request, 'product/cart_detail.html', {'cart': cart})
    except Exception as e:
        return render(request, 'general/error.html', {'message': f'Failed to retrieve cart details: {str(e)}'})


# def add_to_cart_view(request, cart_id, variant_id, qty):
#     response = add_to_cart(cart_id, variant_id, qty)
#     if response.status_code == 200:
#         return redirect('cart_detail', cart_id=cart_id)
#     else:
#         return render(request, 'general/error.html', {'message': 'Failed to add to cart'})

# def remove_from_cart_view(request, cart_id, item_id):
#     response = remove_from_cart(cart_id, item_id)
#     if response.status_code == 200:
#         return redirect('cart_detail', cart_id=cart_id)
#     else:
#         return render(request, 'general/error.html', {'message': 'Failed to remove from cart'})

def cart_detail_view(request):
    cart_id = request.session.get('cart_id')
    #print(cart_id)
    if not cart_id:
        # If there is no cart_id in the session, create one
        region_id = settings.REGION_ID
        #print(region_id)
        cart_response = create_cart()

        request.session['cart_id'] = cart_response['id']

    try:
        cart_response = get_cart_detail(cart_id)
        if cart_response.status_code == 200:
            cart = cart_response.json()['cart']  # Convert response to JSON and extract the 'cart' key
            return render(request, 'order/cart_detail.html', {'cart': cart})
        else:
            return render(request, 'general/error.html',
                          {'message': f'Failed to retrieve cart details. Status code: {cart_response.status_code}'})

    except Exception as e:
        return render(request, 'general/error.html', {'message': f'Failed to retrieve cart details: {str(e)}'})


""" def update_cart_item_view(request, item_id):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return redirect('cart_detail')
    try:
        update_line_item(cart_id, item_id)
        return redirect('cart_detail')
    except Exception as e:
        return render(request, 'general/error.html', {'message': f'Failed to remove item from cart: {str(e)}'})
     """


def update_cart_item_view(request, item_id):
    if request.method == 'POST':
        #print(item_id)
        new_quantity = request.POST.get('quantity')
        cart_id = request.session.get('cart_id')
        if not cart_id:
            return redirect('cart_detail')
        try:
            update_line_item(cart_id, item_id, int(new_quantity))
            return redirect('cart_detail')
        except Exception as e:
            return render(request, 'general/error.html', {'message': f'Failed to update item quantity: {str(e)}'})


def remove_from_cart_view(request, item_id):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return redirect('cart_detail')
    try:
        remove_from_cart(cart_id, item_id)
        return redirect('cart_detail')
    except Exception as e:
        return render(request, 'general/error.html', {'message': f'Failed to remove item from cart: {str(e)}'})


## WORKS
def collections_view(request):
    response = get_collections()
    #print(response.text)  # Print the raw response text for debugging
    if response.status_code == 200:
        collections_data = response.json()
        #print(collections_data)  # Print the parsed JSON response for debugging
        collections = collections_data.get('collections', [])
        return render(request, 'product/collections.html', {'collections': collections})
    else:
        print(f"Failed to load collections: {response.status_code}")  # Print the status code if the request failed
        return render(request, 'general/error.html', {'message': 'Failed to load collections'})


## END WORKS

def collection_products_view(request, collection_id):
    response = get_products(collection_id=collection_id)
    collection = get_collection_name(collection_id)
    #print(collection)
    # products = Product.objects.filter(collection=collection)
    #print(response.text)  # Print the raw response text for debugging
    if response.status_code == 200:
        products_data = response.json()  # Parse the JSON response
        #print(products_data)  # Print the parsed JSON response for debugging
        products = products_data.get('products', [])  # Extract the products list
        return render(request, 'product/collection_products.html',
                      {'collection': collection, 'products': products})  # Pass to template
    else:
        print(f"Failed to load products: {response.status_code}")  # Print the status code if the request failed
        return render(request, 'general/error.html', {'message': 'Failed to load products'})


def update_shipping_view(request, cart_id):
    if request.method == 'POST':
        data = request.POST.dict()
        response = update_shipping_details(cart_id, data)
        if response.status_code == 200:
            return redirect('cart_detail', cart_id=cart_id)
        else:
            return render(request, 'general/error.html', {'message': 'Failed to update shipping details'})
    else:
        return render(request, 'order/update_shipping.html', {'cart_id': cart_id})


def confirm_order_view(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return render(request, 'general/error.html', {'message': 'No cart found. Please add items to your cart first.'})

    response = confirm_order(cart_id)
    if response.status_code == 200:
        order_details = response.json()
        return render(request, 'order/order_confirmation.html', {'order': order_details})
    else:
        message_json = json.loads(response.content.decode('utf-8'))
        # error_message = response.get('error', 'Failed to confirm order')
        error_message = f"{message_json['type']}: {message_json['message']}"
        return render(request, 'general/error.html', {'message': error_message})


def update_cart_view(request, cart_id):
    if request.method == 'POST':
        data = request.POST.dict()
        response = update_cart(cart_id, data)
        if response.status_code == 200:
            return redirect('cart_detail', cart_id=cart_id)
        else:
            return render(request, 'general/error.html', {'message': 'Failed to update cart'})
    else:
        return render(request, 'order/update_cart.html', {'cart_id': cart_id})


# Update Quantity
# def update_cart_item_view(request, variant_id):
#     if request.method == 'POST':
#         new_quantity = request.POST.get('quantity')
#         cart_id = request.session.get('cart_id')
#         coupon_code = request.POST.get('coupon_code')
#         if not cart_id:
#             return redirect('cart_detail')
#         try:
#             data = {
#                 "variant_id": variant_id,
#                 "quantity": new_quantity
#             }
#             updated_cart = update_cart(cart_id, data)
#
#             print(updated_cart.text)
#
#             return redirect('cart_detail')
#         except Exception as e:
#             return render(request, 'general/error.html', {'message': f'Failed to update item quantity: {str(e)}'})


def select_shipping_method_view(request, cart_id):
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        response = shipping_method(cart_id, option_id)
        if response.status_code == 200:
            return redirect('cart_detail', cart_id=cart_id)
        else:
            return render(request, 'general/error.html', {'message': 'Failed to select shipping method'})
    else:
        shipping_options = get_shipping_options(cart_id).json()
        return render(request, 'order/shipping_method.html',
                      {'cart_id': cart_id, 'shipping_options': shipping_options})


def checkout_view(request):
    cart_id = request.session.get('cart_id')
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        
        # If the input doesn't contain an '@', assume it's a username and append @tg.com
        if '@' not in username_or_email:
            email = f"{username_or_email}@tg.com"
        else:
            email = username_or_email
        
        data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'address_1': request.POST.get('address_1'),
            'address_2': request.POST.get('address_2'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'postal_code': request.POST.get('postal_code'),
            'phone': request.POST.get('phone'),
            'email': email  # Use the generated or provided email
        }

        try:
            updated_shipping_details = update_shipping_details(cart_id, data)
            if updated_shipping_details.status_code == 200:
                return redirect('shipping_methods')
            return redirect('shipping_methods')
        except Exception as e:
            return render(request, 'general/error.html', {'message': f'Failed to update shipping details: {str(e)}'})
    
    return render(request, 'order/checkout.html')


# you have to work on this
def remove_qr_payment(method, request, remove_card_id=True):
    if remove_card_id and 'cart_id' in request.session:
        del request.session['cart_id']
    if f'has_{method}_payment' in request.session:
        del request.session[f'has_{method}_payment']
    if 'img_str' in request.session:
        del request.session['img_str']
    if f'{method}_address' in request.session:
        del request.session[f'{method}_address']
    if f'{method}_amount' in request.session:
        del request.session[f'{method}_amount']
    if f'has_{method}_payment' in request.session:
        del request.session[f'has_{method}_payment']


def show_btc_address(request):
    if 'paid' in request.GET:
        remove_qr_payment('btc', request)
        return redirect('cart_detail')

    if request.session.get('has_btc_payment'):
        img_str = request.session.get('img_str')
        btc_address = request.session.get('btc_address')
        btc_amount = request.session.get('btc_amount')
        return render(request, 'order/show_btc_address.html',
                  {'qr_code': img_str, 'btc_address': btc_address, 'amount': btc_amount})


    cart_id = request.session.get('cart_id')
    cart_details = get_cart_detail(cart_id)
    #print("Cart:", cart_details)
    # create and select payment session
    created_payment_session = create_payment_session(cart_id)

    params = {
        'amount': cart_details.json().get('cart').get('total') / 100,
        'currency': cart_details.json().get('cart').get('region').get('currency_code')
    }

    if created_payment_session.status_code == 200:
        selected_payment_session = select_payment_session(cart_id, 'manual')


    # completes the cart
    cart_complete = confirm_order(cart_id)
    #print("Cart ID:", cart_id)
    #print("Cart complete:", cart_complete.json())

    if not cart_complete.json().get('data'):
        return redirect('cart_detail')

    params['metadata'] = {
        'orderId': cart_complete.json().get('data').get('id')
    }

    response = create_payment(params)
    #print("Params", params)

    address_response = get_invoice_details(response.json().get('id'))
    #print(address_response)

    btc_address = address_response.json()[0].get('destination')
    btc_amount = address_response.json()[0].get('amount')

    btc_payment = "bitcoin:"+btc_address+"?amount="+btc_amount

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(btc_payment)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # completes the cart
    cart_complete = confirm_order(cart_id)

    #print('Cart Complete', cart_complete.json())

    del request.session['cart_id']

    request.session['has_btc_payment'] = True
    request.session['img_str'] = img_str
    request.session['btc_address'] = btc_address
    request.session['btc_amount'] = btc_amount

    return render(request, 'order/show_btc_address.html',
                  {'qr_code': img_str, 'btc_address': btc_address, 'amount': btc_amount})


def show_usdt_address(request):

    if 'paid' in request.GET:
        remove_qr_payment('usdt', request)
        return redirect('cart_detail')

    if request.session.get('has_usdt_payment'):
        img_str = request.session.get('img_str')
        usdt_address = request.session.get('usdt_address')
        usdt_amount = request.session.get('usdt_amount')
        return render(request, 'order/show_usdt_address.html',
                  {'qr_code': img_str, 'usdt_address': usdt_address, 'amount': usdt_amount})

    cart_id = request.session.get('cart_id')
    cart_details = get_cart_detail(cart_id)

    # create and select payment session
    created_payment_session = create_payment_session(cart_id)

    if created_payment_session.status_code == 200:
        selected_payment_session = select_payment_session(cart_id, 'manual')

    now_pay_config = {
        "url": settings.USDT_URL,
        "apiKey": settings.USDT_API_KEY,
        "ipn": settings.USDT_IPN
    }

    currency_code = cart_details.json().get('cart').get('region').get('currency_code')

    # completes the cart
    # Confirm the order and get the response JSON
    response_json = confirm_order(cart_id).json()

    # Extract the order ID with default to None if keys are missing
    order_id = response_json.get('data', {}).get('id')
    #print('Cart Complete', cart_complete.json())

    # Get USDT Rate
    conversion_response = requests.get(
        f"https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies={currency_code}"
    )
    conversion_rate = conversion_response.json().get('tether').get(currency_code)

    # Calculate the equivalent amount in USDT (Tether)
    usdt_amount = round((cart_details.json().get('cart').get('total') / 100) / conversion_rate, 8)

    response = requests.post(
        f"{now_pay_config['url']}/v1/payment",
        headers={
            'x-api-key': now_pay_config['apiKey'],
            'Content-Type': 'application/json'
        },
        json={
            "price_amount": usdt_amount,
            "price_currency": cart_details.json().get('cart').get('region').get('currency_code'),
            "pay_currency": "usdttrc20",
            "ipn_callback_url": "https://nowpayments.io",
            "order_id": order_id,
            "order_description": cart_details.json().get('cart').get('email'),
            "is_fixed_rate": True,
            "is_fee_paid_by_user": False,
        }
    )

    usdt_address = response.json().get('pay_address')

    # if not usdt_address:
    #     return redirect('cart_detail')

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(usdt_address)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()


    del request.session['cart_id']

    request.session['has_usdt_payment'] = True
    request.session['img_str'] = img_str
    request.session['usdt_address'] = usdt_address
    request.session['usdt_amount'] = usdt_amount

    return render(request, 'order/show_usdt_address.html',
                  {'qr_code': img_str, 'usdt_address': usdt_address, 'amount': usdt_amount})


def show_xmr_address(request):

    if 'paid' in request.GET:
        remove_qr_payment('xmr', request)
        return redirect('cart_detail')

    if request.session.get('has_xmr_payment'):
        img_str = request.session.get('img_str')
        xmr_address = request.session.get('xmr_address')
        xmr_amount = request.session.get('xmr_amount')
        return render(request, 'order/show_xmr_address.html',
                  {'qr_code': img_str, 'xmr_address': xmr_address, 'amount': xmr_amount})

    cart_id = request.session.get('cart_id')
    cart_details = get_cart_detail(cart_id)

    # create and select payment session
    created_payment_session = create_payment_session(cart_id)

    if created_payment_session.status_code == 200:
        selected_payment_session = select_payment_session(cart_id, 'manual')


    currency_code = cart_details.json().get('cart').get('region').get('currency_code')

    # Get USDT Rate
    conversion_response = requests.get(
        f"https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies={currency_code}"
    )
    conversion_rate = conversion_response.json().get('monero').get(currency_code)

    # Calculate the equivalent amount in USDT (Tether)
    xmr_amount = round((cart_details.json().get('cart').get('total') / 100) / conversion_rate, 8)

    site_settings = SiteSettings.objects.last()
    xmr_address = site_settings.xmr_fixed_address if site_settings else ''

    xmr_payment = "monero:"+xmr_address+"?amount="+str(xmr_amount)
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(xmr_payment)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # completes the cart
    cart_complete = confirm_order(cart_id)

    #print('Cart Complete', cart_complete.json())

    del request.session['cart_id']

    request.session['has_xmr_payment'] = True
    request.session['img_str'] = img_str
    request.session['xmr_address'] = xmr_address
    request.session['xmr_amount'] = xmr_amount

    return render(request, 'order/show_xmr_address.html',
                  {'qr_code': img_str, 'xmr_address': xmr_address, 'amount': xmr_amount})



def show_payment_options(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if payment_method == 'btc':
            return redirect('show_btc_address')
        elif payment_method == 'usdt':
            return redirect('show_usdt_address')
        elif payment_method == 'xmr':
            return redirect('show_xmr_address')

    return render(request, 'order/show_payment_options.html')


def shipping_methods(request):
    if request.method == 'POST':
        cart_id = request.session.get('cart_id')
        selected_option_id = request.POST.get('option_id')
        request.session['selected_option_id'] = selected_option_id
        selected_shipping_method = shipping_method(cart_id, selected_option_id)
        return redirect('show_payment_options')

    cart_id = request.session.get('cart_id')
    available_shipping_methods = get_shipping_options(cart_id)
    return render(request, 'order/shipping_method.html',
                  {'shipping_options': available_shipping_methods.json().get('shipping_options')})


def create_payment_session_view(request, cart_id):
    response = create_payment_session(cart_id)
    if response.status_code == 200:
        return redirect('cart_detail', cart_id=cart_id)
    else:
        return render(request, 'general/general/error.html', {'message': 'Failed to create payment session'})


def select_payment_session_view(request, cart_id):
    if request.method == 'POST':
        provider_id = request.POST.get('provider_id')
        response = select_payment_session(cart_id, provider_id)
        if response.status_code == 200:
            return redirect('cart_detail', cart_id=cart_id)
        else:
            return render(request, 'general/error.html', {'message': 'Failed to select payment session'})
    else:
        # Assuming you have a way to get available payment providers
        payment_providers = [{"id": "provider_1", "name": "Provider 1"}, {"id": "provider_2", "name": "Provider 2"}]
        return render(request, 'order/select_payment_session.html',
                      {'cart_id': cart_id, 'payment_providers': payment_providers})


# def customer_signup(request):
    
#     if request.method == 'POST':

#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             first_name, last_name = generate_random_name()
#             data = {
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'email': form.cleaned_data.get('email'),
#                 'password': form.cleaned_data.get('password')
#             }
#             #print(data)
#             # check if user exists
#             customer = check_email_exists(form.cleaned_data.get('email'))
#             #print(customer.json().get('exists'))

#             if customer.json().get('exists'):
#                 messages.error(request, 'Email already registered! Please log in.')
#             else:
#                 create_customer(data)
#                 messages.success(request, 'Account created successfully! Please log in.')
#                 # Optionally, you can clear the form after successful signup
#                 form = SignUpForm()
#                 return redirect('customer_signin')
#         else:
#             for field in form:
#                 if field.errors:
#                     messages.error(request, f"{field.label} is required")
#     else:
#         form = SignUpForm()

#     return render(request, 'product/customer_signup.html', {'form': form})
def customer_signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Generate random name for first name and last name
            first_name, last_name = generate_random_name()
            username = form.cleaned_data.get('username')
            email = f"{username}@tg.com"
            
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': form.cleaned_data.get('password')
            }

            # Check if user exists
            customer = check_email_exists(email)

            if customer.json().get('exists'):
                messages.error(request, 'Email already registered! Please log in.')
            else:
                create_customer(data)
                messages.success(request, 'Account created successfully! Please log in.')
                # Optionally, you can clear the form after successful signup
                form = SignUpForm()
                return redirect('customer_signin')
        else:
            for field in form:
                if field.errors:
                    messages.error(request, f"{field.label} is required")
    else:
        form = SignUpForm()

    return render(request, 'account/customer_signup.html', {'form': form})



# def customer_signin(request):
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
        
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             email = f"{username}@tg.com"

#             customer = login_jwt(email, password)
            
#             if customer.text == 'Unauthorized':
#                 messages.error(request, 'Incorrect Username or Password')
#                 return redirect('customer_signin')

#             customer_token = customer.json().get('access_token')

#             request.session['auth_token'] = customer_token

#             return redirect('customer_profile')
#     else:
#         form = SignInForm()
        
#     return render(request, 'product/customer_signin.html', {'form': form})
def customer_signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            customer = login_jwt(email, password)
            
            if customer.text == 'Unauthorized':
                messages.error(request, 'Incorrect Email or Password')
                return redirect('customer_signin')

            customer_token = customer.json().get('access_token')

            request.session['auth_token'] = customer_token

            return redirect('customer_profile')
    else:
        form = SignInForm()
        
    return render(request, 'account/customer_signin.html', {'form': form})


@login_required
def customer_profile(request):
    auth_token = request.session.get('auth_token')

    if auth_token:
        # Assuming this function fetches the customer profile using the auth_token
        current_customer = get_customer_profile(auth_token)
        #print(current_customer.json())
        if current_customer.status_code == 200:
            # Extract customer data from the response
            customer_data = current_customer.json().get('customer')

            # Store customer data in session
            request.session['customer_data'] = customer_data
            email = customer_data.get('email')

            # print(email)
            level_data = {
                'customer_username': '',
                'total_points_last_year': '0',
                'level': 'Bronze',
                'total_orders': '0',
                'total_amount': '0',
                'first_joined_date': ''
            }

            # Fetch customer level data using email
            try:
                level_response = get_customer_level(email)
                # Check if the response has a status code and is successful
                if hasattr(level_response, 'status_code') and level_response.status_code == 200:
                    # Extract level data
                    level_data = level_response.json().get('data', level_data)
            except Exception as e:
                print(f"An error occurred: {e}")

            # Render the template with customer and level data
            return render(request, 'account/profile.html', {'customer': customer_data, 'level': level_data})
        else:
            # Handle API response errors or authentication failures
            return render(request, 'account/customer_signin.html')
    else:
        # Redirect to sign-in page if auth_token is not in session
        return redirect('customer_signin')

# def customer_profile(request):
#     auth_token = request.session.get('auth_token')

#     if auth_token:
#         try:
#             # Fetch the customer profile using the auth_token
#             current_customer = get_customer_profile(auth_token)
#             current_customer.raise_for_status()  # Raise an error for unsuccessful status codes

#             # Extract customer data from the response
#             customer_data = current_customer.json().get('customer')
#             request.session['customer_data'] = customer_data
#             email = customer_data.get('email')

#             try:
#                 # Fetch customer level data using email
#                 level_response = get_customer_level(email)
#                 level_response.raise_for_status()

#                 # Extract level data
#                 level_data = level_response.json().get('data')  # Assuming this is where 'customer_username' is located

#             except requests.exceptions.HTTPError as http_err:
#                 print(f"HTTP error occurred while fetching customer level: {http_err}")
#                 level_data = handle_default_level_data()  # Fallback to default level data
#             except requests.exceptions.ConnectionError:
#                 print("Connection error occurred: The level server might be offline.")
#                 level_data = handle_default_level_data()
#             except requests.exceptions.Timeout:
#                 print("Timeout occurred: The level server might be unresponsive.")
#                 level_data = handle_default_level_data()
#             except requests.exceptions.RequestException as req_err:
#                 print(f"An error occurred while fetching customer level: {req_err}")
#                 level_data = handle_default_level_data()

#             # Render the template with customer and level data
#             return render(request, 'account/profile.html', {'customer': customer_data, 'level': level_data})

#         except requests.exceptions.HTTPError as http_err:
#             print(f"HTTP error occurred while fetching customer profile: {http_err}")
#             return render(request, 'account/customer_signin.html')
#         except requests.exceptions.ConnectionError:
#             print("Connection error occurred: The profile server might be offline.")
#             return render(request, 'account/customer_signin.html')
#         except requests.exceptions.Timeout:
#             print("Timeout occurred: The profile server might be unresponsive.")
#             return render(request, 'account/customer_signin.html')
#         except requests.exceptions.RequestException as req_err:
#             print(f"An error occurred while fetching customer profile: {req_err}")
#             return render(request, 'account/customer_signin.html')

#     else:
#         # Redirect to sign-in page if auth_token is not in session
#         return redirect('customer_signin')

def handle_default_level_data():
    """
    Returns default level data when fetching level data fails.
    """
    return {
        'customer_username': '',
        'total_points_last_year': '0',
        'level': 'Bronze',
        'total_orders': '0',
        'total_amount': '0',
        'first_joined_date': ''
    }

@login_required
def customer_logout(request):
    request.session.clear()
    return redirect('customer_signin')


@login_required
def change_password(request):
    auth_token = request.session.get('auth_token')

    if not auth_token:
        return redirect('customer_signin')  # Redirect to sign-in if not authenticated

    if request.method == 'POST':
        form = NewPasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get('password')

            # Call function to change password
            changed_pass = change_customer_password(auth_token, new_password)

            if changed_pass.status_code == 200:
                # Password changed successfully, redirect to sign-in or profile
                return redirect('customer_profile')  # Adjust to your profile view name
            else:
                # Handle errors, optionally show error message
                print("Password change request failed.")
    else:
        form = NewPasswordForm()

    return render(request, 'account/change_customer_password.html', {'form': form})


@login_required
def customer_orders(request):
    auth_token = request.session.get('auth_token')

    if not auth_token:
        return redirect('customer_signin')

    page = request.GET.get('page', 1)
    limit = 10
    offset = (int(page) - 1) * limit

    orders_data = my_orders(auth_token, offset=offset, limit=limit)
    #print("Orders:", orders_data.json())

    orders_list = orders_data.json().get('orders', [])

    total_orders = orders_data.json().get('count', 0)

    paginator = Paginator(orders_list, limit)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(request, 'order/order.html', {'orders': orders, 'total_orders': total_orders, 'page': page})


def add_coupon_code(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        cart_id = request.session.get('cart_id')
        response = update_cart(cart_id, {
            "discounts": [{
                "code": coupon_code
            }]
        })
        #print(response.status_code)
        # Check if the response status code is 400 or 404
        if response.status_code == 400 or response.status_code == 404:
            error_message = response.json().get('message', 'An error occurred')
            # Pass the error message as a URL parameter
            return redirect(f"{reverse('cart_detail')}?error_message={error_message}")

        # If successful, redirect to cart detail
        return redirect('cart_detail')


class PageDetailView(DetailView):
    model = Page
    template_name = 'page/page_detail.html'
    context_object_name = 'page'


class ContactPageView(TemplateView):
    template_name = 'page/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_page = Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            return render(request, 'page/contact_success.html', {'page': contact_page})
        return render(request, self.template_name, {'form': form})
