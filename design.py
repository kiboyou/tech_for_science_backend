JAZZMIN_SETTINGS = {
    "site_title": "ClickHealth Admin",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "ClickHealth",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "ClickHealth Admin",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the ClickHealth Admin Panel",
    # Copyright on the footer
    "copyright": "ClickHealth",

    "show_sidebar": True,
    "navigation_expanded": False,
    # Use modals instead of popups
    "related_modal_active": False,
    "show_ui_builder": True,


    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        #{"name": "NouveauUtilisateur", "url": "utilisateur_nouveaUtilisateur_change", "permissions": ["utilisateur.add_nouveaUtilisateur"]},


        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "utilisateur.NouveauUtilisateur"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        #{"app": "personnel"},
    ],
    "hide_apps": ["utilisateur"],
    # for the full list of 5.13.0 free icon classes
    "icons": {
            # Tableau de bord (Dashboard)
            "dashboard": "fas fa-tachometer-alt",  # Tableau de bord général

            # Utilisateurs
            "utilisateur.NouveauUtilisateur": "fas fa-user-plus",  # Nouvel utilisateur

            # Patients
            "patient.Patient": "fas fa-user-injured",  # Patient

            # Personnel
            "personnel.Medecin": "fas fa-user-md",  # Médecin
            "personnel.Receptionniste": "fas fa-user-tie",  # Réceptionniste
            "personnel.FonctionMedecin": "fas fa-briefcase-medical",  # Fonction d'un médecin
            "personnel.SpecialiteMedecin": "fas fa-user-tag",  # Spécialité médicale
            "personnel.NumeroCaisse": "fas fa-cash-register",  # Numéro de caisse

            # Paiements
            "paiement.Paiement": "fas fa-money-check-alt",  # Paiement

            # Consultations
            "consultation.Consultation": "fas fa-stethoscope",  # Consultation médicale
            "consultation.TypeConsultation": "fas fa-notes-medical",  # Type de consultation

            # Examens
            "examen.Examen": "fas fa-microscope",  # Examen médical
            "examen.TypeExamen": "fas fa-flask",  # Type d'examen

            # Facturation
            "facturation.FacturactionExamen": "fas fa-file-invoice-dollar",  # Facturation d'examen
            "facturation.FactureRendezVous": "fas fa-file-invoice",  # Facture pour rendez-vous

            # Ordonnances
            "ordonnance.Ordonnance": "fas fa-file-prescription",  # Ordonnance
            "ordonnance.TypeOrdonnance": "fas fa-notes-medical",  # Type d'ordonnance
            "ordonnance.Medicament": "fas fa-pills",  # Médicament
            "ordonnance.Presciption": "fas fa-prescription-bottle",  # Prescription

            # Rendez-vous
            "rendezVous.Planning": "fas fa-calendar-alt",  # Planning des rendez-vous
            "rendezVous.RendezVous": "fas fa-calendar-check",  # Rendez-vous confirmé

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
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "utilisateur.NouveauUtilisateur"}
    ],

}