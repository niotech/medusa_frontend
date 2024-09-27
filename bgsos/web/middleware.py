# bgsos/catalog/middleware.py
from django.conf import settings
from web.services.services import MedusaStore

medusa_store = MedusaStore()


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'cart_id' not in request.session:
            try:
                region_id = settings.REGION_ID
                cart = medusa_store.create_cart()
                request.session['cart_id'] = cart['id']
            except Exception as e:
                print(f"Error creating cart: {e}")

        response = self.get_response(request)
        return response
