from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from django.core.mail import EmailMultiAlternatives
from datetime import datetime

def enviar_convite_depoimento(request, depoimento):
    url_feedback = request.build_absolute_uri(
        reverse("feedback_publico", args=[str(depoimento.token)])
    )

    contexto = {
        "cliente": depoimento.cliente,
        "url_feedback": url_feedback,
    }

    assunto = "SolarTech | Conte como foi sua experiência"
    html_message = render_to_string("pages/email_convite_depoimento.html", contexto)
    plain_message = strip_tags(html_message)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    recipient_list = [depoimento.cliente.email]

    send_mail(
        subject=assunto,
        message=plain_message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )

def enviar_orcamento_email(solicitacao, orcamento):
    subject = 'Seu orçamento SolarTech'

    html_content = render_to_string('emails/orcamento_email.html', {
        'solicitacao': solicitacao,
        'orcamento': orcamento,
        'year': datetime.now().year,
    })

    email = EmailMultiAlternatives(
        subject=subject,
        body='Seu cliente de email não suporta HTML.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[solicitacao.cliente.email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()