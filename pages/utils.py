from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime

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