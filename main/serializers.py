from rest_framework import serializers

from .models import (Atelier, AtelierImage, BlogImage, BlogPost,
                     ContactMessage, EstablishmentRequest, SponsorApplication,
                     TeamMember, VolunteerApplication)


class AtelierImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtelierImage
        fields = ("id", "image_url", "caption", "order")


class AtelierSerializer(serializers.ModelSerializer):
    images = AtelierImageSerializer(many=True, required=False)
    class Meta:
        model = Atelier
        fields = "__all__"

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        atelier = Atelier.objects.create(**validated_data)
        for img in images_data:
            AtelierImage.objects.create(atelier=atelier, **img)
        return atelier

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if images_data is not None:
            instance.images.all().delete()
            for img in images_data:
                AtelierImage.objects.create(atelier=instance, **img)
        return instance


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ("id", "image_url", "caption", "order")


class BlogPostSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, required=False)
    class Meta:
        model = BlogPost
        fields = "__all__"

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        post = BlogPost.objects.create(**validated_data)
        for img in images_data:
            BlogImage.objects.create(post=post, **img)
        return post

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if images_data is not None:
            instance.images.all().delete()
            for img in images_data:
                BlogImage.objects.create(post=instance, **img)
        return instance


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"


 


# --- Form submissions ---
class VolunteerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerApplication
        fields = "__all__"


class SponsorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorApplication
        fields = "__all__"


class EstablishmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentRequest
        fields = "__all__"


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
 
