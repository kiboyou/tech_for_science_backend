from django.db import models
from django.utils import timezone
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (Atelier, BlogPost, ContactMessage, EstablishmentRequest,
                     Info, SponsorApplication, TeamMember,
                     VolunteerApplication)
from .serializers import (AtelierSerializer, BlogPostSerializer,
                          ContactMessageSerializer,
                          EstablishmentRequestSerializer, InfoSerializer,
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

	@action(detail=False, methods=["get"], url_path="promoted")
	def promoted(self, request):
		qs = self.get_queryset().filter(is_published=True, is_promoted=True)
		serializer = self.get_serializer(qs, many=True)
		return Response(serializer.data)


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


class InfoViewSet(BaseModelViewSet):
	queryset = Info.objects.filter(is_published=True)
	serializer_class = InfoSerializer
	search_fields = ["title", "excerpt", "content", "procedure"]
	ordering_fields = ["deadline", "created_at", "title"]
	lookup_field = "slug"

	def get_queryset(self):
		qs = super().get_queryset()
		t = self.request.query_params.get("info_type")
		if t:
			qs = qs.filter(info_type=t)
		return qs

	@action(detail=False, methods=["get"], url_path="promoted")
	def promoted(self, request):
		now = timezone.now()
		qs = self.get_queryset().filter(
			is_promoted=True
		).filter(
			models.Q(promote_start__isnull=True) | models.Q(promote_start__lte=now),
			models.Q(promote_end__isnull=True) | models.Q(promote_end__gte=now),
		)
		serializer = self.get_serializer(qs, many=True)
		return Response(serializer.data)


 


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
 
 
