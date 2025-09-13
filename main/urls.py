from rest_framework.routers import DefaultRouter

from .views import (AtelierViewSet, BlogPostViewSet, ContactMessageViewSet,
                    EstablishmentRequestViewSet, SponsorApplicationViewSet,
                    TeamMemberViewSet, VolunteerApplicationViewSet)

router = DefaultRouter()
router.register(r'ateliers', AtelierViewSet, basename='atelier')
router.register(r'blog', BlogPostViewSet, basename='blog')
router.register(r'equipe', TeamMemberViewSet, basename='equipe')
router.register(r'forms/benevoles', VolunteerApplicationViewSet, basename='form-benevoles')
router.register(r'forms/sponsors', SponsorApplicationViewSet, basename='form-sponsors')
router.register(r'forms/etablissements', EstablishmentRequestViewSet, basename='form-etablissements')
router.register(r'forms/contact', ContactMessageViewSet, basename='form-contact')

urlpatterns = router.urls
