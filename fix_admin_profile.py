import os
# pyrefly: ignore [missing-import]
import django   

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

# pyrefly: ignore [missing-import]
from django.contrib.auth.models import User
from mi_aplicacion.models import PerfilMiembro

admin_user = User.objects.filter(username='admin').first()
if admin_user:
    perfil, created = PerfilMiembro.objects.get_or_create(user=admin_user)
    perfil.es_admin = True
    perfil.save()
    print("Perfil de admin actualizado/creado con es_admin=True")
else:
    print("Usuario admin no encontrado")
