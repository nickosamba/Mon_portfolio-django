from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('apropos/', views.apropos, name = 'about'),
    path('Portfolio/', views.projets, name = 'projets'),
    path('Competences/', views.competences, name = 'competences'),
    path('Formations/', views.formations, name = 'formations'),
    path('Mesexperiences/', views.experiences, name = 'experiences'),
    path('contact/', views.contact, name = 'contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('contact/error/', views.contact_error, name='contact_error'),
    path('commentaires/', views.commentaires_view, name='commentaires'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
