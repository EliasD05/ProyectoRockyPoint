# pyrefly: ignore [missing-import]
from django.urls import path
from .views import (
    HomeView, 
    AdminDashboardView,
    AdminRegistroMiembroView, 
    LoginCustomView, 
    LogoutView,
    DeleteEventoView,
    ToggleAdminView,
    DeleteMiembroView,
    PerfilView,
    MiembrosView
)

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("miembros/", MiembrosView.as_view(), name='miembros'),
    path("admin-dashboard/", AdminDashboardView.as_view(), name='admin_dashboard'),
    path("admin-registro-miembro/", AdminRegistroMiembroView.as_view(), name='admin_registro_miembro'),
    path("login/", LoginCustomView.as_view(), name='custom_login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("evento/eliminar/<int:pk>/", DeleteEventoView.as_view(), name='delete_evento'),
    path("miembro/toggle-admin/<int:pk>/", ToggleAdminView.as_view(), name='toggle_admin'),
    path("miembro/eliminar/<int:pk>/", DeleteMiembroView.as_view(), name='delete_miembro'),
    path("perfil/", PerfilView.as_view(), name='perfil'),
]
