import os
# pyrefly: ignore [missing-import]
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

# pyrefly: ignore [missing-import]
from django.contrib.auth.models import User
users = User.objects.all()
for user in users:
    print(f"User: {user.username}, Email: {user.email}, IsSuper: {user.is_superuser}")
