from django.urls import path, include
from .views import  BlacklistTokenUpdateView, UserConnecter, UtilisateurViewSet, ChangerMotPasseView


urlpatterns = [

     path('', UtilisateurViewSet.as_view({'get': 'list', 'post': 'create'}), name="utilisateur"),
     path('<int:pk>/', UtilisateurViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="utilisateur-detail"),

     path('changer_mot_passe/', ChangerMotPasseView.as_view(), name='change-password'),
     path('connecter/', UserConnecter.as_view(), name='userConncter'),

     path('deconnexion/', BlacklistTokenUpdateView.as_view(),name='blacklist'),
     path('reinitialiser_mot_passe/', include('django_rest_passwordreset.urls', namespace='password_reset'))
]
