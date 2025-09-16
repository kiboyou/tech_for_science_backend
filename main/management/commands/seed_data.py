from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import (Atelier, AtelierImage, BlogImage, BlogPost, Info,
                         TeamMember)


class Command(BaseCommand):
    help = "Seed database with demo data for main app (excluding user)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Seeding demo data..."))

        # Clear existing demo-ish data (safe reset for dev only)
        AtelierImage.objects.all().delete()
        BlogImage.objects.all().delete()
        Atelier.objects.all().delete()
        BlogPost.objects.all().delete()
        TeamMember.objects.all().delete()
        Info.objects.all().delete()

        now = timezone.now()

        # --- Team Members ---
        founder = TeamMember.objects.create(
            name="Fondatrice",
            role="Fondatrice & Directrice",
            bio="Passionnée par les sciences et l’éducation, elle pilote nos programmes.",
            photo="https://res.cloudinary.com/demo/image/upload/w_1200,h_1600,c_fill,g_face,q_auto,f_auto/sample.jpg",
            order=0,
            active=True,
            is_featured=True,
        )
        TeamMember.objects.create(
            name="Coordinateur Ateliers",
            role="Coordination des ateliers",
            bio="Organise les ateliers et coordonne les intervenants.",
            photo="https://res.cloudinary.com/demo/image/upload/w_1200,h_1200,c_fill,g_face,q_auto,f_auto/face_top.jpg",
            order=1,
            active=True,
        )
        TeamMember.objects.create(
            name="Responsable Communication",
            role="Communication",
            bio="En charge de la communication et des relations partenaires.",
            photo="https://res.cloudinary.com/demo/image/upload/w_1200,h_1200,c_fill,g_face,q_auto,f_auto/face_center.jpg",
            order=2,
            active=True,
        )

        # --- Ateliers ---
        at1 = Atelier.objects.create(
            title="Atelier Robotique pour Collégiens",
            summary="Initiation à la robotique et programmation.",
            content="Découverte des capteurs, moteurs et algorithmes de base.",
            cover_image="https://res.cloudinary.com/demo/image/upload/w_1600,h_900,c_fill,q_auto,f_auto/tech/robotics.jpg",
            start_date=now + timedelta(days=14),
            end_date=now + timedelta(days=14, hours=2),
            location="Dakar",
            is_published=True,
            is_promoted=True,
        )
        AtelierImage.objects.create(
            atelier=at1,
            image_url="https://res.cloudinary.com/demo/image/upload/w_1200,h_800,c_fill,q_auto,f_auto/tech/robot_arm.jpg",
            caption="Assemblage du robot",
            order=1,
        )
        AtelierImage.objects.create(
            atelier=at1,
            image_url="https://res.cloudinary.com/demo/image/upload/w_1200,h_800,c_fill,q_auto,f_auto/tech/kids_robot.jpg",
            caption="Programmation en équipe",
            order=2,
        )

        Atelier.objects.create(
            title="Initiation à l’Astronomie",
            summary="Observer le ciel et comprendre les étoiles.",
            content="Utilisation de télescopes et lecture de cartes du ciel.",
            cover_image="https://res.cloudinary.com/demo/image/upload/w_1600,h_900,c_fill,q_auto,f_auto/space/stars.jpg",
            start_date=now + timedelta(days=30),
            end_date=now + timedelta(days=30, hours=2),
            location="Thiès",
            is_published=True,
            is_promoted=False,
        )

        # --- Blog Posts ---
        bp1 = BlogPost.objects.create(
            title="Retour sur l’atelier robotique",
            excerpt="Une journée de découvertes et de sourires.",
            content="Les participants ont assemblé et programmé des robots simples.",
            cover_image="https://res.cloudinary.com/demo/image/upload/w_1600,h_900,c_fill,q_auto,f_auto/tech/robot_team.jpg",
            published_at=now - timedelta(days=10),
            is_published=True,
        )
        BlogImage.objects.create(
            post=bp1,
            image_url="https://res.cloudinary.com/demo/image/upload/w_1200,h_800,c_fill,q_auto,f_auto/tech/robot_close.jpg",
            caption="Détail du montage",
            order=1,
        )

        BlogPost.objects.create(
            title="Pourquoi l’astronomie émerveille",
            excerpt="Lever les yeux vers le ciel, c’est rêver et apprendre.",
            content="Les constellations et la Voie lactée comme portes d’entrée.",
            cover_image="https://res.cloudinary.com/demo/image/upload/w_1600,h_900,c_fill,q_auto,f_auto/space/milky_way.jpg",
            published_at=now - timedelta(days=3),
            is_published=True,
        )

        # --- Infos ---
        Info.objects.create(
            title="Concours Jeunes Scientifiques 2025",
            info_type="concours",
            excerpt="Participez au concours national et remportez des prix.",
            content="Ouvert aux lycéens avec projets scientifiques innovants.",
            procedure="Candidature en ligne, présélection, finale régionale.",
            link_url="https://example.org/concours",
            deadline=now + timedelta(days=45),
            cover_image="https://res.cloudinary.com/demo/image/upload/w_1600,h_900,c_fill,q_auto,f_auto/science/lab.jpg",
            is_published=True,
            is_promoted=True,
            promote_start=now - timedelta(days=1),
            promote_end=now + timedelta(days=15),
        )
        Info.objects.create(
            title="Bourses Étudiantes STEM",
            info_type="bourse",
            excerpt="Soutien financier pour études en sciences et technologies.",
            content="Dossier académique, lettre de motivation, références.",
            procedure="Soumission en ligne, entretien, attribution.",
            link_url="https://example.org/bourses",
            deadline=now + timedelta(days=60),
            cover_image="https://res.cloudinary.com/demo/image/upload/w_1600,h_900,c_fill,q_auto,f_auto/education/students.jpg",
            is_published=True,
            is_promoted=False,
        )

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
