from django.urls import path
from . import views

urlpatterns = [
    path('planes/', views.planes, name='planes'),
    path('checkout/<str:plan_id>/', views.checkout, name='checkout'),
    path('success/', views.success, name='payment_success'),
    path('cancel/', views.cancel, name='payment_cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]