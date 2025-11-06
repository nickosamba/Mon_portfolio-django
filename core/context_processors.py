from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

def public_user(request):
    User = get_user_model()
    try:
        user = User.objects.first()
    except (OperationalError, ProgrammingError):
        user = None
    return {'user': user}

def active_page(request):
    return {
        'page': request.resolver_match.url_name
    }
