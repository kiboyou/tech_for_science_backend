from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS, IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from utils import generate_password, send_custom_email
from .serializer import UtilisateurSerializer, ChangerMotPasseSerializer, InfoUserSerializer, GroupSerializer
from .models import NouveauUtilisateur



class IsOwnerOrReadOnly(BasePermission):
    def has_object_permissions(self, request, view, obj):
        if request.method in SAFE_METHODS:
          return True
        return obj.owner == request.user


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser|IsOwnerOrReadOnly|IsAuthenticated]


class UtilisateurViewSet(ModelViewSet):
    queryset = NouveauUtilisateur.objects.filter(is_archived=False).order_by('-date_creation')
    serializer_class = UtilisateurSerializer
    permission_classes = [IsAdminUser|IsOwnerOrReadOnly|IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        user_group = data.get('groups')[0]
        user_name = data.get('first_name')

        # Génération d'un mot de passe temporaire selon le format spécifié
        temporary_password = generate_password(user_group, user_name)

        data['password'] = make_password(temporary_password)

        # Sérialisation et sauvegarde de l'utilisateur
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Envoi d'un e-mail avec le mot de passe temporaire
        send_custom_email('Votre mot de passe temporaire',
                          f'Bonjour {user.first_name},\n\n Votre mot de passe temporaire est : {temporary_password}\n Veuillez le changer lors de votre première connexion.',
                          [user.email])

        # Réponse de succès avec les détails de l'utilisateur
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        utilisateur = self.get_object()
        utilisateur.is_archived = True
        utilisateur.date_archived = timezone.now()  # Optionnel : pour ajouter une date d'archivage
        utilisateur.save()

        return Response(
            {"status": "success", "message": "L'utilisateur a été supprimer avec succès."},
            status=status.HTTP_204_NO_CONTENT
        )




class ChangerMotPasseView(UpdateAPIView):
     serializer_class = ChangerMotPasseSerializer
     model = NouveauUtilisateur
     permission_classes = (IsAuthenticated,)


     def get_object(self, queryset=None):
          obj = self.request.user
          return obj


     def put(self, request, *args, **kwargs):
          self.object = self.get_object()
          serializer = self.get_serializer(data=request.data)

          if serializer.is_valid():
               if not self.object.check_password(serializer.data.get("ancien_password")):
                    return Response({"ancien_password": ["Mauvais mot de passe"]}, status=status.HTTP_400_BAD_REQUEST)

               self.object.set_password(serializer.data.get("nouveau_password"))
               self.object.is_password_changed = True
               self.object.save()

               # Envoi de l'email de confirmation
               send_custom_email('Votre mot de passe a été modifié',
                          'Bonjour, \n\nVotre mot de passe a été modifié avec succès. Si vous n\'êtes pas à l\'origine de cette modification, veuillez nous contacter immédiatement.',
                          [self.object.email])

               response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'votre mot de passe modifier avec succes',
                    'data': []
               }
               return Response(response)


class UserConnecter(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = InfoUserSerializer
    def get_object(self):
        return self.request.user


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        # Récupère le refresh_token depuis les données envoyées
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            # Si aucun refresh_token n'est trouvé, renvoie un message d'erreur clair
            return Response({"error": "Le refresh_token est requis pour la déconnexion."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Met le token sur liste noire
            return Response({"message": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Le token n'est pas valide ou une erreur est survenue."},
                            status=status.HTTP_400_BAD_REQUEST)