# utils.py
import random
import string

from decouple import config
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError


def generate_password(user_group, user_name, length=10):
    # Prendre les 3 premières lettres du groupe de l'utilisateur
    group_letters = user_group[:3]

    # Prendre les 2 premières lettres du nom de l'utilisateur
    name_letters = user_name[:4]

    # Générer 3 chiffres aléatoires
    random_digits = ''.join(random.choice(string.digits) for _ in range(3))

    # Combiner le tout pour former le mot de passe
    password = group_letters + name_letters + random_digits

    # Si la longueur du mot de passe est supérieure à 8, on peut ajouter des caractères supplémentaires
    if len(password) < length:
        characters = string.ascii_letters + string.digits + string.punctuation
        password += ''.join(random.choice(characters) for _ in range(length - len(password)))

    return password



def send_custom_email(subject, message, recipient_list):
    """
    Fonction pour envoyer un email personnalisé.

    :param subject: Le sujet de l'email.
    :param message: Le contenu de l'email.
    :param recipient_list: Liste des destinataires de l'email.
    """
    try:
        send_mail(
            subject,       # Sujet de l'email
            message,       # Contenu de l'email
            settings.EMAIL_HOST_USER,  # Adresse email de l'expéditeur
            recipient_list,  # Liste des destinataires
            fail_silently=False,  # Si une erreur se produit, elle est levée
        )
        print(f"Email envoyé à {recipient_list}")
    except Exception as e:
        # Gestion des erreurs d'envoi d'email si nécessaire
        print(f"Erreur lors de l'envoi de l'email: {e}")

