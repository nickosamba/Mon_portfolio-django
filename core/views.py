from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import *
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from  django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Commentaire
from .forms import CommentaireForm

# Create your views here.
def home(request): 
    # User = CustomUser.objects.first()
    # context = {'User': User}
    return render(request, 'core/home.html')

def apropos(request):
    user = CustomUser.objects.get(is_superuser=True)
    skills = Skill.objects.all()
    
    context = {
        'user': user,
        'skills': skills
    }
    return render(request, 'core/about.html', context)

def projets(request):
    projets = Project.objects.all()
    
    context = {'projets': projets} 
    return render(request, 'core/projects.html', context)

def competences(request):
    competences = Skill.objects.all()

    categories = {
        "Frontend": {
            "label": "Frontend Development",
            "color": "blue",
            "icon": """
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 18l6-6-6-6M8 6l-6 6 6 6"/>
                </svg>
            """
        },
        "Backend": {
            "label": "Backend Development",
            "color": "green",
            "icon": """
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                </svg>
            """
        },
        "Mobile": {
            "label": "Mobile Development",
            "color": "purple",
            "icon": """
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <rect x="7" y="2" width="10" height="20" rx="2" ry="2"/>
                  <circle cx="12" cy="18" r="1"/>
                </svg>
            """
        },
        "Réseau": {
            "label": "Réseau",
            "color": "blue",
            "icon": """
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M12 2v2m0 16v2m10-10h-2M4 12H2m15.364-7.364l-1.414 1.414M6.05 17.95l-1.414 1.414M17.95 17.95l1.414 1.414M6.05 6.05L4.636 4.636"/>
                </svg>
            """
        },
        "Système": {
            "label": "Systèmes",
            "color": "yellow",
            "icon": """
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path d="M9.75 3L9 4.5 7.5 5.25 9 6l.75 1.5L12 6l.75-1.5L12 3zM15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path d="M19.4 15a1.5 1.5 0 110-2.9 1.5 1.5 0 010 2.9zM4.6 15a1.5 1.5 0 110-2.9 1.5 1.5 0 010 2.9z"/>
                </svg>
            """
        },
        "IA": {
            "label": "Intelligence Artificielle",
            "color": "pink",
            "icon": """
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path d="M12 4a8 8 0 100 16 8 8 0 000-16z"/>
                  <path d="M12 9v3l2 2"/>
                </svg>
            """
        },
    }

    return render(request, "core/skills.html", {
        "competences": competences,
        "categories": categories,
    })


def formations(request):
    formations = Formation.objects.all()
    context = {'formations': formations}
    return render(request, 'core/formations.html', context)

def experiences(request):
    experiences = Experience.objects.all()
    context = {'experiences': experiences}
    return render(request, 'core/experience.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        content = request.POST.get('message')
        
        # Vérification des champs obligatoires
        if not all([name, prenom, email, subject, content]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return redirect('core:contact')
        # Vérification du format de l'email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Adresse email invalide.")
            return redirect('core:contact')

        # Validation simple
        if name and prenom and email and content:
            try:
                Message.objects.create(name=name, prenom = prenom, email=email, content=content)
                           # Format du message
                message_body = f"""
                -----------------------------------------------------------------
                MESSAGE DE CONTACT DU PORTFOLIO
                -----------------------------------------------------------------
                
                Prénom : {prenom}
                Nom : {name}
                Email : {email}
                Sujet : {subject}
                

                Message :
                {content}
                """
                # Envoi de l'email
                send_mail(
                    subject=f"Message de {name} : {subject}",
                    message=message_body,
                    from_email='3x.ingenieur@gmail.com',
                    recipient_list=['nickosamba.nh21@gmail.com'],
                )

                return redirect('core:contact_success')
            except Exception as e:
                print("Erreur d'envoi :", e)
                return redirect('core:contact_error')
    return render(request, 'core/contact.html')
    

def contact_success(request):
    return render(request, 'core/contact_success.html')

def contact_error(request):
    return render(request, 'core/contact_error.html')



#commentaire
def commentaires_view(request):
    commentaires = Commentaire.objects.order_by('-date')
    form = CommentaireForm()

    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:commentaires')  # nom de l'URL

    return render(request, 'core/commentaires.html', {
        'form': form,
        'commentaires': commentaires
    })

