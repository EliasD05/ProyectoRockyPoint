# pyrefly: ignore [missing-import]
from django.contrib import admin
from mi_aplicacion.models import Solicitud, PerfilMiembro

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'cedula', 'fecha_creacion', 'aprobada')
    list_filter = ('aprobada', 'disciplina', 'grupo_sanguineo')
    search_fields = ('nombres', 'apellidos', 'cedula', 'email_contacto')

@admin.register(PerfilMiembro)
class PerfilMiembroAdmin(admin.ModelAdmin):
    list_display = ('user', 'es_admin')
    list_filter = ('es_admin',)
