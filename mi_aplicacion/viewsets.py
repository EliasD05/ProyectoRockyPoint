# pyrefly: ignore [missing-import]
from django.contrib.auth.models import Group, Permission, User
# pyrefly: ignore [missing-import]
from rest_framework import viewsets
from mi_aplicacion.models import Solicitud, PerfilMiembro
from mi_aplicacion.serializers import (
    GroupSerializer, 
    PermissionSerializer,
    UserSerializer,
    SolicitudSerializer,
    PerfilMiembroSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

class PerfilMiembroViewSet(viewsets.ModelViewSet):
    queryset = PerfilMiembro.objects.all()
    serializer_class = PerfilMiembroSerializer
