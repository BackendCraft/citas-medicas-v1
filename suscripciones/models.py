from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    PLAN_CHOICES = [
        ('free', 'Gratuito'),
        ('premium', 'Premium'),
    ]
    
    nombre = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField()
    
    def __str__(self):
        return f"Plan {self.get_nombre_display()} - ${self.precio}"

class Suscripcion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_renovacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Suscripción de {self.usuario.username} - {self.plan.get_nombre_display()}"