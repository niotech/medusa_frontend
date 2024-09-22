import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException

import urllib3
from urllib3.util.retry import Retry
from django.conf import settings  # Import settings from Django

class MedusaAdminAPI():
    # Get the variables from the settings
    backendUrl = settings.BACKEND_URL
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


    def __init__(self):
        self.session = requests.Session()
        self.timeout = urllib3.util.Timeout(connect=5.0, read=10.0)

        retry = Retry(
            total=3,
            read=3,
            connect=3,
            backoff_factor=1,
            status_forcelist=[502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)

        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        # self.session.headers.update({'x-publishable-api-key': publishableApiKey})


        # Comment out to disable proxy
        self.session.proxies.update(self.proxies)

        self.auth_token = settings.MEDUSA_ADMIN_TOKEN
        self.incomplete_orders = []


    def login_jwt(self):
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'email': settings.MEDUSA_ADMIN_EMAIL,
            'password': settings.MEDUSA_ADMIN_PASSWORD,
        }
        response = self.session.post(f'{self.backendUrl}/admin/auth/token', headers=headers, json=data)
        if response.text == 'Unauthorized':
            print('Fail to login_jwt')
            return False

        self.auth_token = response.json().get('access_token')
        return True


    def get_incomplete_orders(self):
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
        }

        response = self.session.get(f'{self.backendUrl}/admin/orders?payment_status[]=awaiting&payment_status[]=not_paid&payment_status[]=requires_action', headers=headers)
        if response.json().get('count') == 0:
            print('No incomplete orders found')

        self.incomplete_orders = response.json().get('orders')


    def capture_btc_payment(self):
        self.get_incomplete_orders()

        if len(self.incomplete_orders) == 0:
            print('There is no incomplete order to check on BTC Invoces')
            return False

        # make order_id query params
        param_orderId = ""
        for order in self.incomplete_orders:
            param_orderId += f"orderId={order['id']}&"

        headers = {
            "Authorization": f"token {self.btc_store_api}",
            "Content-Type": "application/json",
        }
        response = requests.get(f'{self.btc_url}/api/v1/stores/{self.btc_store_id}/invoices?{param_orderId}status=Settled', headers=headers)

        if response.status_code == 200:

            settled_orders = response.json()

            if len(settled_orders) == 0:
                print(f"No incomplete orders to be settled!")
                return False

            headers = {
                'Authorization': f'Bearer {self.auth_token}',
            }
            for settled_order in settled_orders:
                orderId = settled_order['metadata']['orderId']
                print(f'Processing Order Id = {orderId}')
                # update medusa, payment_status = captured
                response = session.post(f'{self.backendUrl}/admin/orders/{orderId}/capture', headers=headers)
                if response.status_code == 200:
                    print(f'Order Id = {orderId} Payment Captured')
                else:
                    print(f'Order Id = {orderId} Payment Still Pending')
        else:
            print(f"Requesting BTC Invoices got {response.status_code}")







