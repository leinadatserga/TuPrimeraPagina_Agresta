from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import UsuarioSistema


class formularioCliente(forms.Form):
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
    """Formulario simple para registrar nuevos usuarios"""
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
        email = self.cleaned_data['email']
        if UsuarioSistema.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email

    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        if UsuarioSistema.objects.filter(usuario=usuario).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return usuario

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        if password1 and len(password1) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        
        return cleaned_data


class formularioLogin(forms.Form):
    """Formulario simple para login"""
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


