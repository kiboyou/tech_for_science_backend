from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Atelier, AtelierImage, BlogImage, BlogPost,
                     ContactMessage, EstablishmentRequest, TeamMember,
                     VolunteerApplication)


class AtelierImageForm(forms.ModelForm):
	class Meta:
		model = AtelierImage
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["image_url"].help_text = mark_safe(
			'Collez ici l\'URL Cloudinary (ex: https://res.cloudinary.com/...). '
			'<a href="https://console.cloudinary.com/" target="_blank">Ouvrir Cloudinary</a>'
		)
		self.fields["caption"].help_text = "Légende facultative de l'image."


class AtelierImageInline(admin.TabularInline):
	model = AtelierImage
	extra = 1
	form = AtelierImageForm
	readonly_fields = ["preview"]

	def preview(self, obj):
		if obj.image_url:
			return mark_safe(f'<a href="{obj.image_url}" target="_blank"><img src="{obj.image_url}" style="max-height:60px;max-width:120px;border-radius:6px;border:1px solid #eee;" /></a>')
		return ""
	preview.short_description = "Aperçu"


class AtelierForm(forms.ModelForm):
	class Meta:
		model = Atelier
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		link = '<a href="https://console.cloudinary.com/" target="_blank">Ouvrir Cloudinary</a>'
		self.fields["cover_image"].help_text = mark_safe(
			f"Collez ici l'URL Cloudinary de l'image de couverture. {link}"
		)
		if "video_url" in self.fields:
			self.fields["video_url"].help_text = mark_safe(
				f"Collez ici l'URL Cloudinary de la vidéo. {link}"
			)
		self.fields["summary"].help_text = "Résumé de l'atelier."
		self.fields["content"].help_text = "Contenu détaillé de l'atelier."


@admin.register(Atelier)
class AtelierAdmin(admin.ModelAdmin):
	list_display = ("title", "start_date", "end_date", "location", "is_published")
	list_filter = ("is_published", "start_date")
	search_fields = ("title", "summary", "content", "location")
	prepopulated_fields = {"slug": ("title",)}
	form = AtelierForm
	inlines = [AtelierImageInline]


class BlogImageForm(forms.ModelForm):
	class Meta:
		model = BlogImage
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["image_url"].help_text = mark_safe(
			'Collez ici l\'URL Cloudinary (ex: https://res.cloudinary.com/...). '
			'<a href="https://console.cloudinary.com/" target="_blank">Ouvrir Cloudinary</a>'
		)
		self.fields["caption"].help_text = "Légende facultative de l'image."


class BlogImageInline(admin.TabularInline):
	model = BlogImage
	extra = 1
	form = BlogImageForm
	readonly_fields = ["preview"]

	def preview(self, obj):
		if obj.image_url:
			return mark_safe(f'<a href="{obj.image_url}" target="_blank"><img src="{obj.image_url}" style="max-height:60px;max-width:120px;border-radius:6px;border:1px solid #eee;" /></a>')
		return ""
	preview.short_description = "Aperçu"


class BlogPostForm(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		link = '<a href="https://console.cloudinary.com/" target="_blank">Ouvrir Cloudinary</a>'
		self.fields["cover_image"].help_text = mark_safe(
			f"Collez ici l'URL Cloudinary de l'image de couverture. {link}"
		)
		if "video_url" in self.fields:
			self.fields["video_url"].help_text = mark_safe(
				f"Collez ici l'URL Cloudinary de la vidéo. {link}"
			)
		self.fields["excerpt"].help_text = "Extrait de l'article."
		self.fields["content"].help_text = "Contenu détaillé de l'article."


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ("title", "published_at", "is_published")
	list_filter = ("is_published", "published_at")
	search_fields = ("title", "excerpt", "content")
	prepopulated_fields = {"slug": ("title",)}
	form = BlogPostForm
	inlines = [BlogImageInline]


class TeamMemberForm(forms.ModelForm):
	class Meta:
		model = TeamMember
		fields = "__all__"
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["photo"].help_text = mark_safe(
			'Collez ici l\'URL Cloudinary de la photo du membre. '
			'<a href="https://console.cloudinary.com/" target="_blank">Ouvrir Cloudinary</a>'
		)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
	list_display = ("name", "role", "order", "active")
	list_filter = ("active",)
	search_fields = ("name", "role", "bio", "email")
	ordering = ("order", "name")
	form = TeamMemberForm


 


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "city", "domain", "created_at")
	search_fields = ("name", "email", "city", "domain")
	readonly_fields = ("created_at", "updated_at")


 


@admin.register(EstablishmentRequest)
class EstablishmentRequestAdmin(admin.ModelAdmin):
	list_display = ("establishment_name", "responsible_name", "email", "created_at")
	search_fields = ("establishment_name", "responsible_name", "email")
	readonly_fields = ("created_at", "updated_at")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "subject", "created_at")
	search_fields = ("name", "email", "subject")
	readonly_fields = ("created_at", "updated_at")
