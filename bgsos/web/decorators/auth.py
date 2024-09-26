from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from web.services.services import get_customer_profile, customer_logout as medusa_customer_logout


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'auth_token' not in request.COOKIES:
            return redirect(reverse('customer_signin'))

        # check on medusa for user
        response = get_customer_profile(request.COOKIES['auth_token'])
        if response.status_code != 200:
            medusa_customer_logout(request.COOKIES['auth_token'])
            request.session.clear()
            response = redirect(reverse('customer_signin'))
            response.delete_cookie('auth_token')
            return response

        return view_func(request, *args, **kwargs)

    return wrapper
