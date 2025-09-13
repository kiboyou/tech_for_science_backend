from rest_framework import filters, permissions, viewsets

from .models import (Atelier, BlogPost, ContactMessage, EstablishmentRequest,
                     SponsorApplication, TeamMember, VolunteerApplication)
from .serializers import (AtelierSerializer, BlogPostSerializer,
                          ContactMessageSerializer,
                          EstablishmentRequestSerializer,
                          SponsorApplicationSerializer, TeamMemberSerializer,
                          VolunteerApplicationSerializer)


class PublicReadPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		# Allow read-only for unauthenticated; write requires auth
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user and request.user.is_authenticated


class BaseModelViewSet(viewsets.ModelViewSet):
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	permission_classes = [PublicReadPermission]


class CreateOpenViewSet(viewsets.ModelViewSet):
	# Public endpoint for form submissions: no auth, POST-only
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	authentication_classes: list = []
	http_method_names = ["post"]
	def get_permissions(self):
		return [permissions.AllowAny()]


class AtelierViewSet(BaseModelViewSet):
	queryset = Atelier.objects.all().prefetch_related("images")
	serializer_class = AtelierSerializer
	search_fields = ["title", "summary", "content", "location"]
	ordering_fields = ["start_date", "created_at", "title"]
	lookup_field = "slug"


class BlogPostViewSet(BaseModelViewSet):
	queryset = BlogPost.objects.all().prefetch_related("images")
	serializer_class = BlogPostSerializer
	search_fields = ["title", "excerpt", "content"]
	ordering_fields = ["published_at", "created_at", "title"]
	lookup_field = "slug"


class TeamMemberViewSet(BaseModelViewSet):
	queryset = TeamMember.objects.filter(active=True)
	serializer_class = TeamMemberSerializer
	search_fields = ["name", "role", "bio", "email"]
	ordering_fields = ["order", "name", "created_at"]


 


class VolunteerApplicationViewSet(CreateOpenViewSet):
	queryset = VolunteerApplication.objects.all()
	serializer_class = VolunteerApplicationSerializer
	search_fields = ["name", "email", "city", "domain"]
	ordering_fields = ["created_at", "name"]


class SponsorApplicationViewSet(CreateOpenViewSet):
	queryset = SponsorApplication.objects.all()
	serializer_class = SponsorApplicationSerializer
	search_fields = ["org_name", "contact_name", "email"]
	ordering_fields = ["created_at", "org_name"]


class EstablishmentRequestViewSet(CreateOpenViewSet):
	queryset = EstablishmentRequest.objects.all()
	serializer_class = EstablishmentRequestSerializer
	search_fields = ["establishment_name", "responsible_name", "email"]
	ordering_fields = ["created_at", "establishment_name"]


class ContactMessageViewSet(CreateOpenViewSet):
	queryset = ContactMessage.objects.all()
	serializer_class = ContactMessageSerializer
	search_fields = ["name", "email", "subject"]
	ordering_fields = ["created_at", "name"]
 
