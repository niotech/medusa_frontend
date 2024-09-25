# In catalog/context_processors.py
from web.services.services import get_collections
from .models import SiteSettings, FooterNav

def cart_id(request):
    return {'cart_id': request.session.get('cart_id')}

def collections_processor(request):
    response = get_collections()
    if response.status_code == 200:
        collections_data = response.json()
        collections = collections_data.get('collections', [])
    else:
        collections = []
    return {'collections': collections}

def auth_token_processor(request):
    #print(request.session.get('auth_token'))
    return {
        'auth_token_exists': request.session.get('auth_token') is not None
    }

def site_settings(request):
    settings = SiteSettings.objects.last()
    return {
        'site_settings': settings
    }


def footer_nav_items(request):
    return {
        'footer_nav_items': FooterNav.objects.all()
    }