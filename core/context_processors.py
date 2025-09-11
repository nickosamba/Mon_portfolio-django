from django.contrib.auth import get_user_model

def active_page(request):
    return {
        'page': request.resolver_match.url_name
    }

def public_user(request):
    User = get_user_model()
    user = User.objects.first()  # ou filtre selon ton logique
    return {'user': user}