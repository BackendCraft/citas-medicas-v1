from django.contrib import admin
from .models import Plan, Suscripcion

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'plan', 'activo', 'fecha_inicio', 'fecha_renovacion')
    list_filter = ('activo', 'plan')
    search_fields = ('usuario__username', 'stripe_customer_id')