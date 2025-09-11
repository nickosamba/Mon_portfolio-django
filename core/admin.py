from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profil', {'fields': ('biographie','titrepersonnel','localisation', 'photo','profile_public', 'cv_pdf')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Formation)
admin.site.register(Message)
admin.site.register(Commentaire)
admin.site.site_header = "Administration du Portfolio"
admin.site.site_title = "Admin Portfolio"
admin.site.index_title = "Tableau de bord de l'administration"
# Register your models here.
