from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.dateformat import DateFormat
import tinify
from django.conf import settings
import os

tinify.key = settings.TINIFY_API_KEY 
from cloudinary.models import CloudinaryField

# Extension du modèle User pour ajouter biographie et photo de profil
class CustomUser(AbstractUser):
    titrepersonnel = models.CharField(max_length=100, blank = True, null = True, default='full')
    biographie = models.TextField(blank=True)
    #photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    photo = CloudinaryField('image', folder='profile', blank=True, null=True)
    #profile_public = models.ImageField(upload_to='profile/public/', blank=True, null=True)
    
    profile_public = CloudinaryField('image', folder='profile/public', blank=True, null=True)
    localisation = models.CharField(max_length=100, blank = True, null = True, default= 'brazzaville')
    cv_pdf = models.FileField(upload_to='cv/', blank=True, null=True)
    
    
    #compresser
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        def compress_image(image_field):
            if image_field and image_field.path.lower().endswith((".jpg", ".jpeg", ".png")):
                try:
                    source = tinify.from_file(image_field.path)
                    source.to_file(image_field.path)
                    print(f"Image compressée : {image_field.path}")
                except tinify.Error as e:
                    print(f" Erreur TinyPNG : {e}")

        compress_image(self.photo)
        compress_image(self.profile_public)
        
# Modèle Projet
class Project(models.Model):
    STATUS = [("En cours", "En cours"), ("Terminé", "Terminé")]
    title = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.CharField(max_length=100)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices= STATUS, default="En cours")
    created_at = models.DateTimeField(auto_now_add=True)
    
    #compresser
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        def compress_image(image_field):
            if image_field and image_field.path.lower().endswith((".jpg", ".jpeg", ".png")):
                try:
                    source = tinify.from_file(image_field.path)
                    source.to_file(image_field.path)
                    print(f"Image compressée : {image_field.path}")
                except tinify.Error as e:
                    print(f" Erreur TinyPNG : {e}")

        compress_image(self.image)
    

    def __str__(self):
        return self.title
    @property
    def tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',')]

# Modèle Compétence
class Skill(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Débutant'),
        ('Intermediate', 'Intermédiaire'),
        ('Avanced', 'Avancé'),
        ('Expert', 'Expert'),
    ]
    CATEGORIES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Full-stack', 'Full-stack'),
        ('Mobile', 'Mobile'),
        ('Cloud & DevOps', 'Cloud & DevOps'),
        ('IA', 'Intelligence Artificielle'),
        ('Réseau', 'Réseau'),
        ('Système', 'Système'),
        ('Unix', 'Unix'),
        ('base de données', 'Base de données'),
        ('Sécurité', 'Sécurité'),
        ('Autre', 'Autre'),
        ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=500, choices=CATEGORIES) # ex: "Frontend", "Backend"
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES) # ex: "Débutant", "Intermédiaire", "Expert"

    def __str__(self):
        return f"{self.name} ({self.level})"
    
    #    def period(self):
    #     if self.category == 'Frontend':
    #         badge_color = "green"
    #     elif self.end_date and self.type == 'Backend':
    #         badge_color = "blue"
    #     elif self.end_date and self.type == 'Full-stack':
    #         badge_color = "purple"
    #     elif self.end_date and self.type == 'Mobile': 
    #         badge_color = "yellow"
    #     elif self.end_date and self.type == 'Cloud & DevOps':
    #         badge_color = "cyan"
    #     elif self.end_date and self.type == 'IA':
    #         badge_color = "pink"
    #     elif self.end_date and self.type == 'Réseau':
    #         badge_color = "orange"
    #     elif self.end_date and self.type == 'Système': 
    #         badge_color = "red"
    #     elif self.end_date and self.type == 'Unix':
    #         badge_color = "gray"
    #     else:
    #         badge_color = "yellow"
    #     return {
    #         "text": self.get_category_display(),
    #         "color": badge_color
    #     }
    
    def level_percent(self):
        mapping = {
            'Beginner': 30,
            'Intermediate': 50,
            'Avanced': 75,
            'Expert': 90
        }
        return mapping.get(self.level, 0)


# Modèle Expérience
class Experience(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank = True, null = True)
    start_date = models.DateField(blank = True, null = True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    responsibilities = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} chez {self.company}"
    
    def period(self):
        start = DateFormat(self.start_date).format('F Y')
        if self.end_date:
            end = DateFormat(self.end_date).format('F Y')
        else:
            end = "Présent"
        return f"{start} – {end}"
      

# Modèle Formation
class Formation(models.Model):
    TYPE_CHOICES = [
        ('Diplôme', 'Diplôme'),
        ('Certificat', 'Certificat'),
        ("Formation_suivie_(non certifiée)", "Formation suivie (non certifiée)"),
        ("Formation_suivie_(certificat en attente)", "Formation suivie (certificat en attente)"),
        ("Formation en auto-apprentissage", "Formation en auto-apprentissage"),
        ('Autre', 'Autre'),
    ]
    
    diploma = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    localisation = models.CharField(max_length=100, default="Brazzaville, Congo")
    description = models.TextField(blank=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Diplôme')
    tags = models.CharField(max_length=255, blank=True)  # Exemple : "Algorithmes,Bases de données,IA"
    

    def __str__(self):
        return f"{self.diploma} à {self.institution}"
    
    def get_tags(self):
         return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    
    def period(self):
        start = DateFormat(self.start_date).format('Y')
        if self.end_date and self.type == 'Diplôme':
            end = DateFormat(self.end_date).format('Y')
            status = "Diplôme obtenu"
            badge_color = "green"
        elif self.end_date and self.type == 'Certificat':
            end = DateFormat(self.end_date).format('Y')
            status = "Certificat obtenu"
            badge_color = "blue"
        elif self.end_date and self.type == "Formation_suivie_(non certifiée)":
            end = DateFormat(self.end_date).format('Y')
            status = "Formation suivie (non certifiée)"
            badge_color = "red"
        elif self.end_date and self.type == "Formation_suivie_(certificat en attente)":
            end = DateFormat(self.end_date).format('Y')
            status = "Formation suivie (certificat en attente)"
            badge_color = "yellow"
        elif self.end_date and self.type == "Formation en auto-apprentissage":
            end = DateFormat(self.end_date).format('Y')
            status = "Formation en auto-apprentissage"
            badge_color = "purple"
        elif self.end_date and self.type == 'Autre':
            end = DateFormat(self.end_date).format('Y')
            status = "Autre"
            badge_color = "gray"
            
        else:
            end = "Présent"
            status = "En cours"
            badge_color = "yellow"
        return {
            "text": f"{start} – {end}",
            "status": status,
            "color": badge_color
        }
    

# Modèle Message (contact)
class Message(models.Model):
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, default="nicko")
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    def send(self):
        """Marquer le message comme envoyé"""
        self.sent_at = timezone.now()   # on met la date/heure actuelle
        self.save()

    def __str__(self):
        return f"Message de {self.name} ({self.email})"


class Commentaire(models.Model):
    nom = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.date.strftime('%d/%m/%Y %H:%M')}"