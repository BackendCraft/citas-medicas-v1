import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Plan, Suscripcion

stripe.api_key = settings.STRIPE_SECRET_KEY

def planes(request):
    planes = Plan.objects.all()
    return render(request, 'suscripciones/planes.html', {
        'planes': planes,
        'stripe_key': settings.STRIPE_PUBLISHABLE_KEY
    })

#@login_required
def checkout(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)

    try:
        # 💡 Datos simulados para pruebas
        fake_email = "cliente_test@ejemplo.com"
        fake_name = "Usuario Demo"

        # Crear cliente en Stripe
        customer = stripe.Customer.create(
            email=fake_email,
            name=fake_name,
            metadata={'plan_id': plan.id}
        )

        # Crear sesión de pago
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer=customer.id,
            line_items=[{
                'price_data': {
                    'currency': 'mxn',
                    'product_data': {
                        'name': f"Plan {plan.get_nombre_display()}",
                        'description': plan.descripcion or "Suscripción básica"
                    },
                    'unit_amount': int(plan.precio * 100),  # en centavos
                    'recurring': {
                        'interval': 'month',
                    }
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri('/suscripciones/success/'),
            cancel_url=request.build_absolute_uri('/suscripciones/cancel/'),
        )

        return redirect(session.url, code=303)

    except Exception as e:
        return HttpResponse(f"Error al crear sesión de Stripe: {str(e)}", status=500)

#@login_required
def success(request):
    return render(request, 'suscripciones/success.html')

@login_required
def cancel(request):
    return render(request, 'suscripciones/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    # Manejar el evento
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        fulfill_order(session)
    elif event['type'] == 'invoice.paid':
        invoice = event['data']['object']
        # Actualizar la fecha de renovación
        update_subscription_renewal(invoice)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # Marcar la suscripción como inactiva
        cancel_subscription(subscription)
    
    return HttpResponse(status=200)

def fulfill_order(session):
    customer_id = session['customer']
    subscription_id = session['subscription']
    
    try:
        # Obtener el usuario asociado al customer
        suscripcion = Suscripcion.objects.get(stripe_customer_id=customer_id)
        
        # Actualizar la suscripción con el ID de suscripción de Stripe
        suscripcion.stripe_subscription_id = subscription_id
        suscripcion.activo = True
        suscripcion.save()
    except Suscripcion.DoesNotExist:
        # Si no existe la suscripción, puede ser un nuevo cliente
        # Aquí habría que manejar la lógica para este caso
        pass

def update_subscription_renewal(invoice):
    subscription_id = invoice['subscription']
    try:
        suscripcion = Suscripcion.objects.get(stripe_subscription_id=subscription_id)
        # Actualiza la fecha de renovación basada en el periodo de facturación
        subscription = stripe.Subscription.retrieve(subscription_id)
        suscripcion.fecha_renovacion = subscription['current_period_end']
        suscripcion.save()
    except Suscripcion.DoesNotExist:
        pass

def cancel_subscription(subscription):
    subscription_id = subscription['id']
    try:
        suscripcion = Suscripcion.objects.get(stripe_subscription_id=subscription_id)
        suscripcion.activo = False
        suscripcion.save()
    except Suscripcion.DoesNotExist:
        pass