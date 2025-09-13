from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import NouveauUtilisateur


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UtilisateurSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.all(),
        slug_field='name'
    )

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = NouveauUtilisateur
        fields = (
        'id', 'email', 'first_name', 'last_name', 'groups', 'password', 'is_password_changed', 'is_active', 'is_staff', 'is_superuser','is_archived')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)  # Assurez-vous que cela correspond au bon champ

        # Assurez-vous que les groupes sont fournis
        if not groups_data:
            raise ValueError("Un groupe doit être spécifié pour l'utilisateur")

        utilisateur = self.Meta.model(**validated_data)

        utilisateur.save()
        # Associez les groupes après la sauvegarde de l'utilisateur
        utilisateur.groups.set(groups_data)
        return utilisateur

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        groups_data = validated_data.pop('groups', None)

        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if password:
            instance.set_password(password)

        if groups_data is not None:  # Vérifiez si des groupes sont fournis
            instance.groups.set(groups_data)

        instance.save()
        return instance


class InfoUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = NouveauUtilisateur
        fields = ['id', 'email', 'first_name', 'last_name', 'groups', 'is_password_changed', 'is_active', 'is_staff', 'is_archived']


class ChangerMotPasseSerializer(serializers.Serializer):
     ancien_password = serializers.CharField(required=True)
     nouveau_password = serializers.CharField(required=True)

     class Meta:
          model = NouveauUtilisateur
          fields = ['ancien_password', 'nouveau_password']

     def validate_ancien_password(self, value):
          user = self.context['request'].user
          if not user.check_password(value):
               raise serializers.ValidationError("Mauvais mot de passe")
          return value