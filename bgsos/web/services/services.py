import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException

import urllib3
from urllib3.util.retry import Retry
from django.conf import settings  # Import settings from Django

# Get the variables from the settings
backendUrl = settings.BACKEND_URL
levelsUrl = settings.LEVELS_URL
auth_token_level = settings.LEVELS_API_KEY
publishableApiKey = settings.MEDUSA_API_KEY
regionId = settings.REGION_ID
btc_url = settings.BTC_URL
btc_store_id = settings.BTC_STORE_ID
btc_store_api = settings.BTC_STORE_API

# Setting up the SOCKS5 proxy
# Comment out to disable proxy

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050',
}


# Creating a session and configuring it
session = requests.Session()

timeout = urllib3.util.Timeout(connect=5.0, read=10.0)

# Adding retry strategy
retry = Retry(
    total=3,
    read=3,
    connect=3,
    backoff_factor=1,
    status_forcelist=[502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)

# Mounting the adapter to session
session.mount('http://', adapter)
session.mount('https://', adapter)

# Setting default headers and proxy configuration
session.headers.update({'x-publishable-api-key': publishableApiKey})


# Comment out to disable proxy
session.proxies.update(proxies)

def create_cart():
    response = session.post(f'{backendUrl}/store/carts')
    if response.status_code == 200:
        cart_data = response.json()
        cart = cart_data.get('cart')
        if cart:
            return cart
        else:
            raise Exception("Cart creation failed, no cart data returned")
    else:
        raise Exception(f"Failed to create cart: {response.status_code}, {response.text}")


def add_to_cart(cart_id, variant_id, qty):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/line-items',
                        json={'variant_id': variant_id, 'quantity': qty})


def update_line_item(cart_id, line_id, quantity):
    url = f'{backendUrl}/store/carts/{cart_id}/line-items/{line_id}'
    response = session.post(url, json={"quantity": quantity})
    response.raise_for_status()
    return response.json()


def remove_from_cart(cart_id, item_id):
    return session.delete(f'{backendUrl}/store/carts/{cart_id}/line-items/{item_id}')


def get_cart_detail(cart_id):
    return session.get(f'{backendUrl}/store/carts/{cart_id}')


def update_line_item(cart_id, line_id, quantity):
    url = f'{backendUrl}/store/carts/{cart_id}/line-items/{line_id}'
    response = session.post(url, json={"quantity": quantity})
    response.raise_for_status()
    return response.json()


def update_cart(cart_id, data):
    return session.post(f'{backendUrl}/store/carts/{cart_id}', json=data)


def get_products(product_id=None, collection_id=None, limit=None):
    params = {}
    if collection_id:
        params['collection_id[]'] = collection_id
    if limit:
        params['limit'] = limit

    if product_id:
        return session.get(f'{backendUrl}/store/products/{product_id}')
    elif collection_id:
        return session.get(f'{backendUrl}/store/products', params=params)
    else:
        return session.get(f'{backendUrl}/store/products')


def browse_all_products():
    return session.get(f'{backendUrl}/store/products')


def get_featured_products(featured_title, limit):
    response = get_collections()
    collections = []
    if response.status_code == 200:
        collections = response.json().get('collections', [])

    for collection in collections:
        name = get_collection_name(collection['id'])
        if name and name == featured_title:
            response = get_products(collection_id=collection['id'], limit=limit)
            if response.status_code == 200:
                products_data = response.json()
                return products_data.get('products', [])
            else:
                return []

    # assume fallback to non Featued products
    response = get_products(limit=limit)
    if response.status_code == 200:
        products_data = response.json()
        return products_data.get('products', [])
    else:
        return []


def get_collections():
    return session.get(f'{backendUrl}/store/collections')


def get_collection_name(id):
    response = session.get(f'{backendUrl}/store/collections/{id}')
    if response.status_code == 200:
        collection_data = response.json()
        return collection_data['collection']['title']  # Extract the title
    else:
        return None


def update_shipping_details(cart_id, data):
    headers = {
        'Content-Type': 'application/json'
    }
    return session.post(f'{backendUrl}/store/carts/{cart_id}', headers=headers, json={
        "shipping_address": {
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
            "address_1": data.get('address_1'),
            "address_2": data.get('address_2'),
            "city": data.get('city'),
            "province": data.get('state'),
            "postal_code": data.get('postal_code'),
            "phone": data.get('phone'),
            "country_code": "au"
        },
        "billing_address": {
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
            "address_1": data.get('address_1'),
            "address_2": data.get('address_2'),
            "city": data.get('city'),
            "province": data.get('state'),
            "postal_code": data.get('postal_code'),
            "phone": data.get('phone'),
            "country_code": "au"
        },
        "email": data.get('email')
    })


def confirm_order(cart_id):
    print('CartId', cart_id)
    return session.post(f'{backendUrl}/store/carts/{cart_id}/complete')


def update_line_item(cart_id, line_id, quantity):
    url = f'{backendUrl}/store/carts/{cart_id}/line-items/{line_id}'
    response = session.post(url, json={"quantity": quantity})
    response.raise_for_status()
    return response.json()


def update_cart(cart_id, data):
    return session.post(f'{backendUrl}/store/carts/{cart_id}', json=data)


def shipping_method(cart_id, option_id):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/shipping-methods', json={'option_id': option_id})


def create_payment_session(cart_id):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/payment-sessions')


def select_payment_session(cart_id, provider_id):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/payment-session', json={'provider_id': provider_id})


def get_shipping_options(cart_id):
    return session.get(f'{backendUrl}/store/shipping-options/{cart_id}')


# New authentication functions

def get_current_customer(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    return session.get(f'{backendUrl}/store/auth', headers=headers)


def create_payment(params):
    url = f"{btc_url}/api/v1/stores/{btc_store_id}/invoices"
    headers = {
        "Authorization": f"token {btc_store_api}",
        "Content-Type": "application/json",
    }
    data = {
        "amount": params['amount'],
        "currency": params['currency'],
        "metadata": params.get('metadata', None)
    }
    return requests.post(url, headers=headers, json=data)


def get_invoice_details(invoice_id):
    url = f"{btc_url}/api/v1/stores/{btc_store_id}/invoices/{invoice_id}/payment-methods"
    headers = {
        "Authorization": f"token {btc_store_api}",
        "Content-Type": "application/json",
    }
    return requests.get(url, headers=headers)


def customer_login(email, password):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'email': email,
        'password': password,
    }
    return session.post(f'{backendUrl}/store/auth', headers=headers, json=data, timeout=timeout)


def customer_logout(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    return session.delete(f'{backendUrl}/store/auth', headers=headers)


def login_jwt(email, password):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'email': email,
        'password': password,
    }
    return session.post(f'{backendUrl}/store/auth/token', headers=headers, json=data)


def check_email_exists(email):
    return session.get(f'{backendUrl}/store/auth/{email}')


def create_customer(data):
    headers = {
        'Content-Type': 'application/json'
    }
    data: data
    return session.post(f'{backendUrl}/store/customers', headers=headers, json=data)


def get_customer_profile(auth_token):
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    return session.get(f'{backendUrl}/store/customers/me', headers=headers)


def change_customer_password(auth_token, new_password):
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    data = {
        'password': new_password
    }
    return session.post(f'{backendUrl}/store/customers/me', headers=headers, json=data)


def get_customer_level(username):
    headers = {
        'Authorization': f'Basic {auth_token_level}'
    }
    
    try:
        response = session.get(f'{levelsUrl}/api/public/customerdetail?username={username}', headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
        return response.json()  # Return the JSON data if the request is successful
    except requests.ConnectionError:
        # Handle connection errors like broken proxies, unreachable hosts
        print("Connection error occurred. Could not reach the customer details API.")
    except requests.Timeout:
        # Handle request timeout errors
        print("The request timed out while trying to reach the customer details API.")
    except requests.RequestException as e:
        # Generic exception handling for all other request-related issues
        print(f"An error occurred: {e}")
    
    # Fallback in case of error, return None or a default value
    return None

# def get_customer_level(email):
#     headers = {
#         'Authorization': f'Basic {auth_token_level}'
#     }
#     try:
#         response = session.get(
#             f'{levelsUrl}/api/public/customerdetail?username={email}',
#             headers=headers,
#             timeout=10
#         )
#         # Check if the response is not None before proceeding
#         if response is not None:
#             response.raise_for_status()  # Raises an HTTPError for bad responses
#             return response.json()  # Assuming the response is JSON and you want to return the parsed JSON data
#         else:
#             print("No response received from the server.")
        
#         #response.raise_for_status()  # Raises an HTTPError for bad responses
#         #return response
#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error occurred: {http_err}")  # Log specific HTTP error
#     except requests.exceptions.ConnectionError as conn_err:
#         print(f"Connection error occurred: {conn_err}")  # Log connection issues
#     except requests.exceptions.Timeout as timeout_err:
#         print(f"Timeout error occurred: {timeout_err}")  # Log timeout errors
#     except requests.exceptions.RequestException as req_err:
#         print(f"An error occurred while fetching customer level: {req_err}")  # Log any request exception
#     return None

def my_orders(auth_token, offset=0, limit=10):
    #print(auth_token)
    #print("Auth token:", auth_token)
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    #print(f'{backendUrl}/store/customers/me/orders?offset={offset}&limit={limit}')
    return session.get(f'{backendUrl}/store/customers/me/orders?offset={offset}&limit={limit}', headers=headers)
