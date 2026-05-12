# pyrefly: ignore [missing-import]
from django import forms
from django.contrib.auth.models import User
from .models import Solicitud, Evento, PerfilMiembro

class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = PerfilMiembro
        fields = ['nombre_completo', 'foto_perfil', 'descripcion', 'telefono']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Cuéntanos un poco sobre ti y tu pasión por las motos...'}),
            'nombre_completo': forms.TextInput(attrs={'placeholder': 'Tu nombre completo'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: +52 1 644 ...'}),
        }

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'fecha', 'lugar']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Rodada Nocturna'}),
            'fecha': forms.TextInput(attrs={'placeholder': 'Ej: Sábado 15'}),
            'lugar': forms.TextInput(attrs={'placeholder': 'Ej: Plaza Central'}),
        }

class RegistroMiembroForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Nombre de Usuario")
    email = forms.EmailField(label="Correo Electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    es_admin = forms.BooleanField(required=False, label="¿Es Administrador?")

    class Meta:
        model = Solicitud
        fields = '__all__'
        exclude = ['fecha_creacion', 'aprobada']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'comentarios': forms.Textarea(attrs={'rows': 3}),
            'emergencia_direccion': forms.Textarea(attrs={'rows': 2}),
        }
# pyrefly: ignore [missing-import]
from crispy_forms.helper import FormHelper
# pyrefly: ignore [missing-import]
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML

class SolicitudForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'DATOS PERSONALES',
                Row(
                    Column('nombres', css_class='form-group col-md-6 mb-0'),
                    Column('apellidos', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('cedula', css_class='form-group col-md-4 mb-0'),
                    Column('sexo', css_class='form-group col-md-4 mb-0'),
                    Column('edad', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('fecha_nacimiento', css_class='form-group col-md-6 mb-0'),
                    Column('lugar_nacimiento', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'DATOS CONTACTO',
                Row(
                    Column('direccion', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('barrio', css_class='form-group col-md-4 mb-0'),
                    Column('ciudad', css_class='form-group col-md-4 mb-0'),
                    Column('pais', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('codigo_postal', css_class='form-group col-md-3 mb-0'),
                    Column('telefono_habitacion', css_class='form-group col-md-3 mb-0'),
                    Column('telefono_movil', css_class='form-group col-md-3 mb-0'),
                    Column('email_contacto', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'DATOS PROFESIONALES / LABORALES',
                Row(
                    Column('ocupacion', css_class='form-group col-md-4 mb-0'),
                    Column('telefono_trabajo', css_class='form-group col-md-4 mb-0'),
                    Column('email_trabajo', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'INFORMACIÓN O CATEGORIA DE LA DISCIPLINA',
                Row(
                    Column('disciplina', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                'comentarios',
            ),
            Fieldset(
                'REGISTRO DE SALUD',
                Row(
                    Column('grupo_sanguineo', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('alergias', css_class='form-group col-md-2 mb-0'),
                    Column('alergias_especifique', css_class='form-group col-md-10 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('padecimientos', css_class='form-group col-md-2 mb-0'),
                    Column('padecimientos_especifique', css_class='form-group col-md-10 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('tratamiento_medico', css_class='form-group col-md-2 mb-0'),
                    Column('tratamiento_especifique', css_class='form-group col-md-10 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('toma_medicamento', css_class='form-group col-md-2 mb-0'),
                    Column('medicamento_forma_suministro', css_class='form-group col-md-10 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('seguro_medico', css_class='form-group col-md-2 mb-0'),
                    Column('seguro_especifique', css_class='form-group col-md-10 mb-0'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'INFORMACIÓN PARA CASOS DE EMERGENCIA',
                HTML('<p style="color: var(--gray); margin-bottom: 1.5rem;">Persona de contacto principal en caso de emergencia.</p>'),
                Row(
                    Column('emergencia_nombres', css_class='form-group col-md-6 mb-0'),
                    Column('emergencia_apellidos', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('emergencia_parentesco', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('emergencia_direccion', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('emergencia_barrio', css_class='form-group col-md-4 mb-0'),
                    Column('emergencia_ciudad', css_class='form-group col-md-4 mb-0'),
                    Column('emergencia_pais', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('emergencia_codigo_tel', css_class='form-group col-md-3 mb-0'),
                    Column('emergencia_telefono', css_class='form-group col-md-9 mb-0'),
                    css_class='form-row'
                ),
                HTML('<hr style="border-color: var(--glass-border); margin: 2rem 0;">'),
                HTML('<p style="color: var(--gray); margin-bottom: 1.5rem;">Segunda persona de contacto alternativa.</p>'),
                Row(
                    Column('emergencia2_nombres', css_class='form-group col-md-6 mb-0'),
                    Column('emergencia2_apellidos', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('emergencia2_codigo_tel', css_class='form-group col-md-3 mb-0'),
                    Column('emergencia2_telefono', css_class='form-group col-md-9 mb-0'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'MOTO O VEHICULO',
                Row(
                    Column('vehiculo_modelo', css_class='form-group col-md-6 mb-0'),
                    Column('vehiculo_placa', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('moto_modelo', css_class='form-group col-md-6 mb-0'),
                    Column('moto_placa', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'DOCUMENTOS Y SOPORTES DEL VEHICULO',
                HTML('<p style="color: var(--gray); margin-bottom: 1rem;">* Tarjeta de Propiedad * SOAT * Revisión Técnicomecánica * Manifiesto de Importación</p>'),
                HTML('<p style="color: var(--gray); font-size: 0.85rem; margin-bottom: 1.5rem;">Tipos de Archivos aceptados: pdf, jpg, jpeg, png</p>'),
                'documentos_vehiculo',
                'foto_identificacion',
            ),
            Fieldset(
                'ASPECTO LEGAL',
                HTML("""
                <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
                    <h4 style="color: var(--primary); margin-bottom: 1rem;">Liberación de Responsabilidad Social</h4>
                    <p style="color: var(--gray); font-size: 0.9rem; line-height: 1.7;">
                        Yo, portador de la cédula de identidad, declaro que conozco todos los riesgos que involucran las actividades deportivas a motor y que haré uso correcto de las instalaciones autorizadas para la práctica deportiva bajo mi única responsabilidad. Así mismo declaro que exonero de toda responsabilidad Penal, Civil o Administrativa a la empresa ROCKY POINT MC y a las autoridades locales por hechos u accidentes ocurridos antes, durante y después de la práctica deportiva o recreativa que realice.<br><br>
                        Por último, doy autorización para mi traslado a la clínica u hospital más cercano, en caso de presentarse algún accidente y autorizo a los médicos a atenderme debidamente.
                    </p>
                </div>
                """),
                'acepta_responsabilidad',
                HTML("""
                <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; margin-top: 2rem;">
                    <h4 style="color: var(--primary); margin-bottom: 1rem;">Aceptación Tratamiento de Datos</h4>
                    <p style="color: var(--gray); font-size: 0.9rem; line-height: 1.7;">
                        Yo, portador de la cédula de identidad, autorizo a "ROCKY POINT MC", a que conserven en ficheros informáticos y/o en cualquier otro soporte físico los datos personales que le han sido proporcionados de forma voluntaria y a tratar esa información con el objeto que le han sido facilitados, es decir, para la administración y gestión. Asimismo, el firmante declara conocer y aceptar las normas generales de funcionamiento del Club de Motociclismo, de las actividades y aquellas genéricas de funcionamiento. Por su parte "ROCKY POINT MC" informa al firmante que su información personal figura en sus oficinas, en las que podrá solicitar el contenido exacto de ella y en donde podrá ejercer los derechos de rectificación, anulación o modificación que pudiera corresponderle, así como modificar esta autorización en cualquier sentido.
                    </p>
                </div>
                """),
                'acepta_privacidad',
                HTML("""
                <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; margin-top: 2rem;">
                    <h4 style="color: var(--primary); margin-bottom: 1rem;">Permiso de Fotografías</h4>
                    <p style="color: var(--gray); font-size: 0.9rem; line-height: 1.7;">
                        Yo, portador de la cédula de identidad, declaro y autorizo a que "ROCKY POINT MC", pueda realizar fotografías durante las actividades, para su posible utilización en medios de comunicación, redes sociales, soportes informáticos o exhibición en otros medios del centro.
                    </p>
                </div>
                """),
                'acepta_fotografias',
            ),
        )

    class Meta:
        model = Solicitud
        exclude = ['horario_entrenamiento', 'fecha_creacion', 'aprobada', 'firma_conformidad']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'comentarios': forms.Textarea(attrs={'rows': 3}),
            'emergencia_direccion': forms.Textarea(attrs={'rows': 2}),
        }