from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NouveauUtilisateur


class NouveauUtilisateurAdmin(admin.ModelAdmin):
    model = NouveauUtilisateur
    search_fields = ('email', 'last_name', 'first_name', 'groups__name', 'date_archived')  # Utilisez 'groups__name' pour rechercher par le nom du groupe
    list_filter = ('email', 'last_name', 'first_name', 'is_active', 'is_staff', 'is_archived', 'groups', 'date_archived')  # Ajoutez le filtre pour les groupes
    ordering = ('-start_date',)
    list_display = ('email', 'last_name', 'first_name', 'is_active', 'is_staff', 'get_groups', 'is_password_changed', 'is_archived', 'date_archived')  # Utilisez une méthode personnalisée pour afficher les groupes

    fieldsets = (
        (None, {'fields': ('email', 'last_name', 'first_name', 'groups', 'is_password_changed', 'is_archived')}),  # Ajoutez le champ 'groups'
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'last_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff', 'groups', 'is_password_changed', 'is_archived')}
         ),
    )

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])  # Récupère les noms des groupes de l'utilisateur
    get_groups.short_description = 'Groups'  # Titre de la colonne dans l'administration

admin.site.register(NouveauUtilisateur, NouveauUtilisateurAdmin)


