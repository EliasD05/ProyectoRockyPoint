# pyrefly: ignore [missing-import]
from django.db import models
# pyrefly: ignore [missing-import]
from django.contrib.auth.models import User

class Solicitud(models.Model):
    # --- DATOS PERSONALES ---
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True, verbose_name="Documento de Identidad")
    SEXO_CHOICES = [
        ('F', 'Femenino'),
        ('M', 'Masculino'),
    ]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    edad = models.PositiveIntegerField()
    fecha_nacimiento = models.DateField()
    lugar_nacimiento = models.CharField(max_length=200)

    # --- DATOS CONTACTO ---
    direccion = models.TextField()
    barrio = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    telefono_habitacion = models.CharField(max_length=20)
    telefono_movil = models.CharField(max_length=20)
    email_contacto = models.EmailField()

    # --- DATOS PROFESIONALES ---
    ocupacion = models.CharField(max_length=100)
    telefono_trabajo = models.CharField(max_length=20)
    email_trabajo = models.EmailField()

    # --- INFORMACIÓN DISCIPLINA ---
    DISCIPLINAS = [
        ('motocross', 'Motocross'),
        ('motovelocidad', 'Motovelocidad'),
        ('enduro', 'Enduro'),
        ('trial', 'Trial'),
        ('supermotard', 'Supermotard'),
        ('cuatrimotos', 'Cuatrimotos'),
        ('motos_calle', 'Motos de Calle'),
        ('atv', 'ATV'),
        ('carros_4x4', 'Carros 4x4'),
    ]
    disciplina = models.CharField(max_length=50, choices=DISCIPLINAS)
    # Horario se guardará como JSON para manejar la matriz de la imagen
    horario_entrenamiento = models.JSONField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)

    # --- REGISTRO DE SALUD ---
    GRUPOS_SANGUINEOS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    grupo_sanguineo = models.CharField(max_length=5, choices=GRUPOS_SANGUINEOS)
    
    alergias = models.BooleanField(default=False)
    alergias_especifique = models.TextField(null=True, blank=True)
    
    padecimientos = models.BooleanField(default=False)
    padecimientos_especifique = models.TextField(null=True, blank=True)
    
    tratamiento_medico = models.BooleanField(default=False)
    tratamiento_especifique = models.TextField(null=True, blank=True)
    
    toma_medicamento = models.BooleanField(default=False)
    medicamento_forma_suministro = models.TextField(null=True, blank=True)
    
    seguro_medico = models.BooleanField(default=False)
    seguro_especifique = models.TextField(null=True, blank=True)

    # --- INFORMACIÓN PARA CASOS DE EMERGENCIA ---
    emergencia_nombres = models.CharField(max_length=100, blank=True, verbose_name="Nombres (Contacto Emergencia)")
    emergencia_apellidos = models.CharField(max_length=100, blank=True, verbose_name="Apellidos (Contacto Emergencia)")
    emergencia_parentesco = models.CharField(max_length=100, blank=True, verbose_name="Parentesco")
    emergencia_direccion = models.TextField(blank=True, verbose_name="Dirección de Residencia")
    emergencia_barrio = models.CharField(max_length=100, blank=True, verbose_name="Barrio")
    emergencia_ciudad = models.CharField(max_length=100, blank=True, verbose_name="Ciudad")
    emergencia_pais = models.CharField(max_length=100, blank=True, verbose_name="País")
    emergencia_codigo_tel = models.CharField(max_length=10, blank=True, verbose_name="Código Tel.")
    emergencia_telefono = models.CharField(max_length=20, blank=True, verbose_name="Número de Teléfono")

    # Segunda persona de contacto
    emergencia2_nombres = models.CharField(max_length=100, blank=True, verbose_name="Nombres (2do Contacto)")
    emergencia2_apellidos = models.CharField(max_length=100, blank=True, verbose_name="Apellidos (2do Contacto)")
    emergencia2_codigo_tel = models.CharField(max_length=10, blank=True, verbose_name="Código Tel. (2do)")
    emergencia2_telefono = models.CharField(max_length=20, blank=True, verbose_name="Número de Teléfono (2do)")

    # --- MOTO O VEHÍCULO ---
    vehiculo_modelo = models.CharField(max_length=100, verbose_name="Vehículo Modelo")
    vehiculo_placa = models.CharField(max_length=20, verbose_name="Vehículo Placa")
    moto_modelo = models.CharField(max_length=100, verbose_name="Moto Modelo")
    moto_placa = models.CharField(max_length=20, verbose_name="Moto Placa")

    # --- DOCUMENTOS Y SOPORTES DEL VEHÍCULO ---
    documentos_vehiculo = models.FileField(upload_to='documentos/', verbose_name="Adjuntar Documentos del Vehículo")
    foto_identificacion = models.FileField(upload_to='identificaciones/', verbose_name="Adjuntar Foto de Identificación")

    # --- ASPECTO LEGAL ---
    acepta_responsabilidad = models.BooleanField(default=False, verbose_name="Acepto la Liberación de Responsabilidad Social")
    acepta_privacidad = models.BooleanField(default=False, verbose_name="Acepto la Política de Privacidad")
    acepta_fotografias = models.BooleanField(default=False, verbose_name="Acepto el Permiso de Fotografías")
    firma_conformidad = models.TextField(blank=True, null=True, verbose_name="Firma de Conformidad")

    # --- METADATA ---
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobada = models.BooleanField(default=False)

    def __str__(self):
        return f"Solicitud {self.id}: {self.nombres} {self.apellidos}"

class PerfilMiembro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    solicitud = models.OneToOneField(Solicitud, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_completo = models.CharField(max_length=200, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    descripcion = models.TextField(max_length=500, blank=True, verbose_name="Biografía")
    telefono = models.CharField(max_length=20, blank=True)
    es_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.CharField(max_length=100)
    lugar = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


