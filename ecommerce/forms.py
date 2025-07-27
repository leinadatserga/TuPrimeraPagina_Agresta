from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import UsuarioSistema


class formularioCliente(forms.Form):
    """
    Formulario para la creación de nuevos clientes en el sistema.
    Incluye validación de campos obligatorios y formateo de entrada.
    Features:
        - Validación automática de formato de email.
        - Límites de edad realistas.
        - Placeholders informativos para UX.
    """
    name = forms.CharField(
        max_length=100,
        label='Nombre completo',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese el nombre completo del cliente'
        })
    )
    
    age = forms.IntegerField(
        label='Edad',
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ingrese la edad'
        })
    )
    
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com'
        })
    )


class formularioProductos(forms.Form):
    """
    Formulario para la creación y edición de productos en el catálogo.
    Permite definir todos los aspectos de un producto incluyendo precio,
    stock y estado de visibilidad. Incluye validaciones para datos críticos
    como precios negativos y límites de stock.
    Features:
        - Validación de precios no negativos.
        - Campo de descripción opcional con textarea.
        - Control de stock con validación mínima.
        - Estado activo por defecto para nuevos productos.
    """
    nombre = forms.CharField(
        max_length=200,
        label='Nombre del producto',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese el nombre del producto'
        })
    )
    
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        label='Precio',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ingrese el precio',
            'step': '0.01'
        })
    )
    
    descripcion = forms.CharField(
        required=False,
        label='Descripción',
        widget=forms.Textarea(attrs={
            'placeholder': 'Descripción del producto (opcional)',
            'rows': 4
        })
    )
    
    stock = forms.IntegerField(
        min_value=0,
        initial=0,
        label='Stock disponible',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Cantidad en stock'
        })
    )
    
    activo = forms.BooleanField(
        required=False,
        initial=True,
        label='Producto activo',
        widget=forms.CheckboxInput()
    )


class formularioRegistro(forms.Form):
    """
    Formulario para el registro de nuevos usuarios en el sistema.
    Incluye validación completa de unicidad para email y usuario,
    verificación de contraseñas coincidentes y requisitos mínimos
    de seguridad para contraseñas.
    Features:
        - Contraseñas coincidentes.
        - Longitud mínima de contraseña (6 caracteres).
        - Campos de contraseña con widget PasswordInput.
        - Validación de unicidad antes del guardado.
        - Mensajes de error específicos para cada validación.
    """
    usuario = forms.CharField(
        max_length=150,
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario'
        })
    )
    
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com'
        })
    )
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña'
        })
    )
    
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar contraseña'
        })
    )

    def clean_email(self):
        """
        Valida que el email no esté ya registrado en el sistema.
        Features:
            - Verificación de unicidad en la base de datos.
        """
        email = self.cleaned_data['email']
        if UsuarioSistema.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email

    def clean_usuario(self):
        """
        Valida que el nombre de usuario no esté ya en la base de datos.
        Features:
            - Verificación de unicidad en la base de datos.
        """
        usuario = self.cleaned_data['usuario']
        if UsuarioSistema.objects.filter(usuario=usuario).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return usuario

    def clean(self):
        """
        Validación global del formulario de registro.
        Verifica que las contraseñas coincidan y cumplan con los
        requisitos mínimos de seguridad.
        Features:
            - Contraseñas coincidentes.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        if password1 and len(password1) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        
        return cleaned_data


class formularioLogin(forms.Form):
    """
    Formulario para autenticación de usuarios existentes.
    Proporciona una interfaz simple y segura para el inicio de sesión
    utilizando email y contraseña. Compatible con el sistema de
    autenticación personalizado del proyecto.
    Features:
        - Campo del email con validación automática de formato.
        - Placeholders informativos para mejorar UX.
        - No almacena ni muestra contraseñas en texto plano.
        - Validación del formato del email antes del envío.
    """
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com'
        })
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingrese su contraseña'
        })
    )


