from django.contrib import admin
from .models import Cliente, Producto, UsuarioSistema


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email', 'created_at', 'is_vip')
    list_filter = ('age', 'created_at')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def is_vip(self, obj):
        """Mostrar si es cliente VIP"""
        return obj.age > 40
    is_vip.boolean = True
    is_vip.short_description = 'Es VIP'


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'activo', 'created_at')
    list_filter = ('activo', 'created_at')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('created_at',)
    ordering = ('nombre',)
    list_editable = ('precio', 'stock', 'activo')


@admin.register(UsuarioSistema)
class UsuarioSistemaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('usuario', 'email')
    readonly_fields = ('created_at', 'password')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información básica', {
            'fields': ('usuario', 'email', 'is_active')
        }),
        ('Seguridad', {
            'fields': ('password',),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
