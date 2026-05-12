# pyrefly: ignore [missing-import]
from django.contrib.auth.models import User, Group, Permission
# pyrefly: ignore [missing-import]
from rest_framework import serializers
from .models import Solicitud, PerfilMiembro

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "content_type"]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_active"]

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = "__all__"

class PerfilMiembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilMiembro
        fields = "__all__"

