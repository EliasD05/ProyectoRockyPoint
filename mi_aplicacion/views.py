from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Solicitud, PerfilMiembro, Evento
from .forms import EventoForm, PerfilUpdateForm, RegistroMiembroForm

class DeleteEventoView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated or not hasattr(request.user, 'perfilmiembro') or not request.user.perfilmiembro.es_admin:
            messages.error(request, "Acceso denegado.")
            return redirect('home')
        
        evento = get_object_or_404(Evento, pk=pk)
        evento.delete()
        messages.success(request, "Evento eliminado correctamente.")
        return redirect('admin_dashboard')

class ToggleAdminView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated or not hasattr(request.user, 'perfilmiembro') or not request.user.perfilmiembro.es_admin:
            messages.error(request, "Acceso denegado.")
            return redirect('home')
        
        perfil = get_object_or_404(PerfilMiembro, pk=pk)
        if perfil.user == request.user:
            messages.error(request, "No puedes cambiar tu propio rol.")
        else:
            perfil.es_admin = not perfil.es_admin
            perfil.save()
            messages.success(request, f"Rol de {perfil.user.username} actualizado.")
        return redirect('admin_dashboard')

class DeleteMiembroView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated or not hasattr(request.user, 'perfilmiembro') or not request.user.perfilmiembro.es_admin:
            messages.error(request, "Acceso denegado.")
            return redirect('home')
        
        perfil = get_object_or_404(PerfilMiembro, pk=pk)
        if perfil.user == request.user:
            messages.error(request, "No puedes eliminarte a ti mismo.")
        else:
            user = perfil.user
            if perfil.solicitud:
                perfil.solicitud.delete()
            user.delete()
            messages.success(request, "Miembro eliminado correctamente.")
        return redirect('admin_dashboard')

class HomeView(View):
    def get(self, request):
        eventos = Evento.objects.all().order_by('fecha_creacion')
        return render(request, "home.html", {'eventos': eventos})

class AdminDashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated or not hasattr(request.user, 'perfilmiembro') or not request.user.perfilmiembro.es_admin:
            messages.error(request, "Acceso denegado.")
            return redirect('home')
        
        eventos = Evento.objects.all().order_by('-fecha_creacion')
        miembros = PerfilMiembro.objects.all().select_related('user', 'solicitud')
        form_evento = EventoForm()
        
        return render(request, "admin_dashboard.html", {
            'eventos': eventos,
            'miembros': miembros,
            'form_evento': form_evento
        })
    
    def post(self, request):
        if not request.user.is_authenticated or not hasattr(request.user, 'perfilmiembro') or not request.user.perfilmiembro.es_admin:
            return redirect('home')
        
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento agregado correctamente.")
        else:
            messages.error(request, "Error al agregar el evento.")
            
        return redirect('admin_dashboard')

class AdminRegistroMiembroView(View):
    def get(self, request):
        if not request.user.is_authenticated or not hasattr(request.user, 'perfilmiembro') or not request.user.perfilmiembro.es_admin:
            return redirect('home')
        
        form = RegistroMiembroForm()
        hours = [
            "6 am a 7 am", "7 am a 8 am", "9 am a 10 am", "10 am a 11 am",
            "11 am a 12 pm", "12 pm a 1 pm", "1 pm a 2 pm", "3 pm a 4 pm",
            "4 pm a 5 pm", "5 pm a 6 pm", "6 pm a 7 pm", "7 pm a 8 pm", "8 pm a 9 pm"
        ]
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        return render(request, "admin_registro_miembro.html", {
            'form': form,
            'hours': hours,
            'days': days
        })
    
    def post(self, request):
        if not request.user.is_authenticated or not hasattr(request.user, 'perfilmiembro') or not request.user.perfilmiembro.es_admin:
            return redirect('home')
        
        form = RegistroMiembroForm(request.POST, request.FILES)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            es_admin = form.cleaned_data['es_admin']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "El nombre de usuario ya existe.")
                hours = [
                    "6 am a 7 am", "7 am a 8 am", "9 am a 10 am", "10 am a 11 am",
                    "11 am a 12 pm", "12 pm a 1 pm", "1 pm a 2 pm", "3 pm a 4 pm",
                    "4 pm a 5 pm", "5 pm a 6 pm", "6 pm a 7 pm", "7 pm a 8 pm", "8 pm a 9 pm"
                ]
                days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
                return render(request, "admin_registro_miembro.html", {
                    'form': form,
                    'hours': hours,
                    'days': days
                })
            
            solicitud = form.save(commit=False)
            solicitud.aprobada = True
            
            horario_json = {}
            hours = [
                "6 am a 7 am", "7 am a 8 am", "9 am a 10 am", "10 am a 11 am",
                "11 am a 12 pm", "12 pm a 1 pm", "1 pm a 2 pm", "3 pm a 4 pm",
                "4 pm a 5 pm", "5 pm a 6 pm", "6 pm a 7 pm", "7 pm a 8 pm", "8 pm a 9 pm"
            ]
            days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
            
            for h_idx, hour in enumerate(hours, 1):
                horario_json[hour] = {}
                for d_idx, day in enumerate(days, 1):
                    val = request.POST.get(f'schedule_{h_idx}_{d_idx}', 'no_disponible')
                    horario_json[hour][day] = val
            
            solicitud.horario_entrenamiento = horario_json
            solicitud.save()
            
            user = User.objects.create_user(username=username, email=email, password=password)
            
            PerfilMiembro.objects.create(
                user=user,
                solicitud=solicitud,
                es_admin=es_admin,
                nombre_completo=f"{solicitud.nombres} {solicitud.apellidos}"
            )
            
            messages.success(request, f"Miembro {solicitud.nombres} {solicitud.apellidos} registrado con éxito.")
            return redirect('admin_dashboard')
        
        hours = [
            "6 am a 7 am", "7 am a 8 am", "9 am a 10 am", "10 am a 11 am",
            "11 am a 12 pm", "12 pm a 1 pm", "1 pm a 2 pm", "3 pm a 4 pm",
            "4 pm a 5 pm", "5 pm a 6 pm", "6 pm a 7 pm", "7 pm a 8 pm", "8 pm a 9 pm"
        ]
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        return render(request, "admin_registro_miembro.html", {'form': form, 'hours': hours, 'days': days})

class LoginCustomView(View):
    def get(self, request):
        return render(request, "login.html")
    
    def post(self, request):
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Credenciales inválidas.")
            return render(request, "login.html")

class PerfilView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('custom_login')
        
        perfil = get_object_or_404(PerfilMiembro, user=request.user)
        form = PerfilUpdateForm(instance=perfil)
        return render(request, "perfil.html", {'form': form, 'perfil': perfil})
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('custom_login')
        
        perfil = get_object_or_404(PerfilMiembro, user=request.user)
        form = PerfilUpdateForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil')
        return render(request, "perfil.html", {'form': form, 'perfil': perfil})

class MiembrosView(View):
    def get(self, request):
        miembros = PerfilMiembro.objects.all().select_related('user', 'solicitud')
        return render(request, "miembros.html", {'miembros': miembros})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
