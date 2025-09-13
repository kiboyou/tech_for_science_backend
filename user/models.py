from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string

from django.contrib.auth.models import Group


class GestionUtilisateur(BaseUserManager):

    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Le super utilisateur doit avoir is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Le super utilisateur doit avoir is_superuser=True')

        # Créer le super utilisateur sans spécifier de groupe
        user = self.create_user(email, first_name, last_name, password, **other_fields)

        # Ajouter le super utilisateur au groupe "admin"
        group, created = Group.objects.get_or_create(name='administrateur')
        user.groups.add(group)

        return user

    def create_user(self, email, first_name, last_name, password, group=None, **other_fields):
        if not email:
            raise ValueError(_("L'utilisateur doit avoir un email"))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **other_fields
        )
        user.set_password(password)
        user.save()

        # Ajouter l'utilisateur au groupe spécifié
        user.groups.add(group)

        return user


class NouveauUtilisateur(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=128, blank=True)
    is_password_changed = models.BooleanField(default=False)

    start_date = models.DateTimeField(default=timezone.now)
    date_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_archived = models.DateTimeField(blank=True, null=True)

    is_archived = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = GestionUtilisateur()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    def add_to_group(self, group_name):
        """Ajoute l'utilisateur à un groupe existant."""
        try:
            group = Group.objects.get_or_create(name=group_name)
            self.groups.add(group)
        except Group.DoesNotExist:
            raise ValueError(f"Groupe '{group_name}' n'existe pas.")



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.last_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Your Website Title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@yourdomain.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()