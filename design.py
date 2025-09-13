JAZZMIN_SETTINGS = {
    "site_title": "Tech Pour Science – Admin",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Tech Pour Science",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Tech Pour Science",
    # Custom logo (should be in static/media/img_tech_s.png)
    "site_logo": "media/img_tech_s.png",
    "login_logo": "media/img_tech_s.png",
    "site_logo_classes": "img-circle elevation-2",
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Bienvenue dans l'administration Tech Pour Science",
    # Copyright on the footer
    "copyright": "Tech Pour Science",

    "show_sidebar": True,
    "navigation_expanded": True,
    # Use modals instead of popups
    "related_modal_active": True,
    # Cleaner admin (désactiver l'UI builder)
    "show_ui_builder": False,


    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
    {"name": "Accueil",  "url": "admin:index", "permissions": ["auth.view_user"]},
        #{"name": "NouveauUtilisateur", "url": "utilisateur_nouveaUtilisateur_change", "permissions": ["utilisateur.add_nouveaUtilisateur"]},

        # model admin to link to (Permissions checked against model)
        {"model": "utilisateur.NouveauUtilisateur"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        #{"app": "personnel"},
    ],
    "hide_apps": [
        app for app in [
            "auth", "token_blacklist", "django_rest_passwordreset", "drf_yasg", "rest_framework", "admin", "contenttypes", "sessions", "messages", "staticfiles"
        ]
        if app not in ["user", "main"]
    ],
    # Thèmes Bootswatch (clair/sombre)
    "theme": "lux",
    "dark_mode_theme": "darkly",
    # Afficher le sélecteur de langue
    "language_chooser": True,
    # for the full list of 5.13.0 free icon classes
    "icons": {
            # Tableau de bord (Dashboard)
            "dashboard": "fas fa-tachometer-alt",  # Tableau de bord général

            # Utilisateurs
            "utilisateur.NouveauUtilisateur": "fas fa-user-plus",  # Nouvel utilisateur

            
            # Gestion des groupes (auth)
            "auth.Group": "fas fa-users-cog",  # Groupes d'utilisateurs

            # Gestion des tokens (blacklist)
            "token_blacklist.BlacklistedToken": "fas fa-ban",  # Jetons blacklistés
            "token_blacklist.OutstandingToken": "fas fa-key",  # Jetons valides

            # File d'attente
            "fileattente.PatientQueue": "fas fa-user-clock",  # File d'attente des patients

            # Réinitialisation de mot de passe
            "django_rest_passwordreset": "fas fa-unlock-alt",  # Jetons de réinitialisation de mot de passe
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "show_usermenu": False,

}

# Ajustements UI alignés aux couleurs de marque (#f1c016 or/gold, #2dabb2 teal)
JAZZMIN_UI_TWEAKS = {
    # Layout
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "footer_fixed": False,
    "actions_sticky_top": True,

    # Text sizing
    "navbar_small_text": False,
    "sidebar_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,

    # Couleurs (AdminLTE classes)
    "brand_colour": "navbar-warning",  # gold
    "accent": "accent-teal",           # teal
    "navbar": "navbar-warning navbar-dark",
    "no_navbar_border": True,
    "sidebar": "sidebar-dark-warning",

    # Boutons
    "button_classes": "btn btn-sm btn-warning",

    # Sidebar
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
}