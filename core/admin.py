from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'titrepersonnel', 'localisation', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'localisation')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Infos personnelles', {'fields': ('last_name','first_name','titrepersonnel', 'biographie', 'photo', 'profile_public', 'localisation', 'cv_pdf')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level', 'level_percent')
    list_filter = ('category', 'level')
    search_fields = ('name',)

admin.site.register(Skill, SkillAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'featured', 'created_at')
    list_filter = ('status', 'featured')
    search_fields = ('title', 'technologies')
    ordering = ('-created_at',)

admin.site.register(Project, ProjectAdmin)

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date')
    search_fields = ('title', 'company')
    list_filter = ('start_date', 'end_date')

admin.site.register(Experience, ExperienceAdmin)

class FormationAdmin(admin.ModelAdmin):
    list_display = ('diploma', 'institution', 'type', 'start_date', 'end_date')
    search_fields = ('diploma', 'institution')
    list_filter = ('type', 'start_date', 'end_date')

admin.site.register(Formation, FormationAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'prenom', 'email', 'created_at', 'sent_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at', 'sent_at')

admin.site.register(Message,MessageAdmin)

class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'message', 'date')
    search_fields = ('nom', 'message')
    list_filter = ('date',)

admin.site.register(Commentaire,CommentaireAdmin)





admin.site.site_header = "Administration du Portfolio"
admin.site.site_title = "Admin Portfolio"
admin.site.index_title = "Tableau de bord de l'administration"
# Register your models here.
