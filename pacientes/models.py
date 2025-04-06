from django.db import models
from django.utils import timezone

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    TIPO_CITA_CHOICES = [
        ('primera_vez', 'Primera vez'),
        ('seguimiento', 'Seguimiento'),
        ('control', 'Control rutinario'),
        ('urgencia', 'Urgencia'),
    ]
    
    paciente = models.CharField(max_length=100)
    medico = models.CharField(max_length=100)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    tipo_cita = models.CharField(max_length=20, choices=TIPO_CITA_CHOICES, default='control')
    motivo = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    duracion = models.PositiveIntegerField(default=30)
    notas = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cita de {self.paciente} con {self.medico} el {self.fecha} a las {self.hora}"