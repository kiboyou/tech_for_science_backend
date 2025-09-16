from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Atelier(TimeStampedModel):
	title = models.CharField("Titre", max_length=200)
	slug = models.SlugField("Slug", unique=True, max_length=220, blank=True)
	summary = models.TextField("Résumé", blank=True)
	content = models.TextField("Contenu", blank=True)
	cover_image = models.URLField("Image de couverture (Cloudinary)", blank=True, null=True, max_length=500)
	video_url = models.URLField("Vidéo (Cloudinary)", blank=True, null=True, max_length=500)
	start_date = models.DateTimeField("Date de début", blank=True, null=True)
	end_date = models.DateTimeField("Date de fin", blank=True, null=True)
	location = models.CharField("Lieu", max_length=200, blank=True)
	is_published = models.BooleanField("Publié", default=True)
	is_promoted = models.BooleanField("Mis en avant", default=False)

	class Meta:
		ordering = ["-start_date", "-created_at"]
		verbose_name = "Atelier"
		verbose_name_plural = "Ateliers"

	class Meta:
		ordering = ["-start_date", "-created_at"]

	def __str__(self) -> str:
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)[:220]
		super().save(*args, **kwargs)


class BlogPost(TimeStampedModel):
	title = models.CharField("Titre", max_length=200)
	slug = models.SlugField("Slug", unique=True, max_length=220, blank=True)
	excerpt = models.TextField("Extrait", blank=True)
	content = models.TextField("Contenu", blank=True)
	cover_image = models.URLField("Image de couverture (Cloudinary)", blank=True, null=True, max_length=500)
	video_url = models.URLField("Vidéo (Cloudinary)", blank=True, null=True, max_length=500)
	published_at = models.DateTimeField("Date de publication", blank=True, null=True)
	is_published = models.BooleanField("Publié", default=True)

	class Meta:
		ordering = ["-published_at", "-created_at"]
		verbose_name = "Article de blog"
		verbose_name_plural = "Articles de blog"

	class Meta:
		ordering = ["-published_at", "-created_at"]

	def __str__(self) -> str:
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)[:220]
		super().save(*args, **kwargs)


class TeamMember(TimeStampedModel):
	name = models.CharField("Nom", max_length=150)
	role = models.CharField("Rôle", max_length=150, blank=True)
	bio = models.TextField("Bio", blank=True)
	photo = models.URLField("Photo (Cloudinary)", blank=True, null=True, max_length=500)
	email = models.EmailField("Email", blank=True)
	order = models.PositiveIntegerField("Ordre", default=0)
	active = models.BooleanField("Actif", default=True)
	is_featured = models.BooleanField("À la une", default=False)

	class Meta:
		ordering = ["order", "name"]
		verbose_name = "Membre de l'équipe"
		verbose_name_plural = "Membres de l'équipe"

	class Meta:
		ordering = ["order", "name"]

	def __str__(self) -> str:
		return f"{self.name} — {self.role}" if self.role else self.name

 


class AtelierImage(TimeStampedModel):
	atelier = models.ForeignKey(Atelier, related_name="images", on_delete=models.CASCADE, verbose_name="Atelier")
	image_url = models.URLField("Image (Cloudinary)", max_length=500)
	caption = models.CharField("Légende", max_length=200, blank=True)
	order = models.PositiveIntegerField("Ordre", default=0)

	class Meta:
		ordering = ["order", "id"]
		verbose_name = "Image d'atelier"
		verbose_name_plural = "Images d'atelier"

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return f"AtelierImage({self.atelier_id}) #{self.id}"


class BlogImage(TimeStampedModel):
	post = models.ForeignKey(BlogPost, related_name="images", on_delete=models.CASCADE, verbose_name="Article de blog")
	image_url = models.URLField("Image (Cloudinary)", max_length=500)
	caption = models.CharField("Légende", max_length=200, blank=True)
	order = models.PositiveIntegerField("Ordre", default=0)

	class Meta:
		ordering = ["order", "id"]
		verbose_name = "Image d'article de blog"
		verbose_name_plural = "Images d'article de blog"

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return f"BlogImage({self.post_id}) #{self.id}"


class Info(TimeStampedModel):
	TYPE_CHOICES = (
		("concours", "Concours"),
		("bourse", "Bourses"),
		("challenge", "Challenges"),
	)
	# Base
	title = models.CharField("Titre", max_length=200)
	slug = models.SlugField("Slug", unique=True, max_length=220, blank=True)
	info_type = models.CharField("Type", max_length=20, choices=TYPE_CHOICES)
	excerpt = models.TextField("Résumé", blank=True)
	content = models.TextField("Contenu / Détails", blank=True)
	procedure = models.TextField("Procédure / Étapes", blank=True)
	link_url = models.URLField("Lien externe", blank=True, null=True, max_length=500)
	deadline = models.DateTimeField("Date limite", blank=True, null=True)
	cover_image = models.URLField("Image de couverture (Cloudinary)", blank=True, null=True, max_length=500)
	is_published = models.BooleanField("Publié", default=True)
	# Promotion window
	is_promoted = models.BooleanField("Mis en avant", default=False)
	promote_start = models.DateTimeField("Début de promotion", blank=True, null=True)
	promote_end = models.DateTimeField("Fin de promotion", blank=True, null=True)

	class Meta:
		ordering = ["-deadline", "-created_at"]
		verbose_name = "Information (concours/bourse/challenge)"
		verbose_name_plural = "Informations"

	def __str__(self) -> str:
		return f"{self.title} – {self.get_info_type_display()}"

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)[:220]
		super().save(*args, **kwargs)


 


 


# --- Form submissions (public) ---
class VolunteerApplication(TimeStampedModel):
	DOMAIN_CHOICES = (
		("science", "Science"),
		("animation3d", "Animation 3D"),
		("logistique", "Logistique"),
		("communication", "Communication"),
		("administration", "Administration"),
		("autre", "Autre"),
	)
	name = models.CharField("Nom & Prénom", max_length=150)
	email = models.EmailField("Email")
	phone = models.CharField("Téléphone", max_length=50)
	city = models.CharField("Ville / Localisation", max_length=120)
	domain = models.CharField("Domaine de compétences", max_length=30, choices=DOMAIN_CHOICES)
	domain_other = models.CharField("Autre (à préciser)", max_length=200, blank=True)
	availability = models.CharField("Disponibilités (CSV)", max_length=200, blank=True, help_text="Ex: Semaine,Week-end,Vacances scolaires")
	motivation = models.TextField("Pourquoi souhaitez-vous devenir bénévole ?", blank=True)

	class Meta:
		ordering = ["-created_at"]
		verbose_name = "Candidature bénévole"
		verbose_name_plural = "Candidatures bénévoles"

	def __str__(self) -> str:
		return f"{self.name} <{self.email}>"


class SponsorApplication(TimeStampedModel):
	org_name = models.CharField("Organisation / Entreprise", max_length=200)
	contact_name = models.CharField("Nom & Prénom du soumettant", max_length=150)
	role = models.CharField("Fonction", max_length=150, blank=True)
	email = models.EmailField("Email")
	phone = models.CharField("Téléphone", max_length=50)
	support_types = models.CharField("Type de soutien (CSV)", max_length=200, help_text="Institutionnel,Financier,Matériel,Logistique,Bourses,Autre")
	message = models.TextField("Message complémentaire", blank=True)

	class Meta:
		ordering = ["-created_at"]
		verbose_name = "Demande sponsor"
		verbose_name_plural = "Demandes sponsors"

	def __str__(self) -> str:
		return f"{self.org_name} – {self.contact_name}"


class EstablishmentRequest(TimeStampedModel):
	establishment_name = models.CharField("Nom de l’établissement", max_length=200)
	responsible_name = models.CharField("Nom & Prénom du responsable", max_length=150)
	role = models.CharField("Fonction", max_length=150)
	email = models.EmailField("Email")
	phone = models.CharField("Téléphone", max_length=50)
	partnership_types = models.CharField("Type de partenariat souhaité (CSV)", max_length=200, help_text="Ateliers,Conférences,Expositions,Formation,Autre")
	participants = models.PositiveIntegerField("Nombre estimé de participants", null=True, blank=True)
	details = models.TextField("Message / Détails de la demande", blank=True)

	class Meta:
		ordering = ["-created_at"]
		verbose_name = "Demande d’établissement"
		verbose_name_plural = "Demandes d’établissements"

	def __str__(self) -> str:
		return f"{self.establishment_name} – {self.responsible_name}"


class ContactMessage(TimeStampedModel):
	SUBJECT_CHOICES = (
		("question", "Question générale"),
		("partenariat", "Partenariat"),
		("inscription", "Inscription"),
		("autre", "Autre"),
	)
	name = models.CharField("Nom & Prénom", max_length=150)
	email = models.EmailField("Email")
	phone = models.CharField("Téléphone", max_length=50, blank=True)
	subject = models.CharField("Sujet", max_length=20, choices=SUBJECT_CHOICES)
	message = models.TextField("Message")

	class Meta:
		ordering = ["-created_at"]
		verbose_name = "Message de contact"
		verbose_name_plural = "Messages de contact"

	def __str__(self) -> str:
		return f"{self.name} – {self.subject}"
