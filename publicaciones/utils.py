from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def notificar(publicacion, cambio, razon=""):
    subject = 'Cambio en tu Publicación'
    recipient_list = [publicacion.autor.email]
    from_email=settings.EMAIL_HOST_USER
    email_content = render_to_string('publicaciones/email.html', {
        'publicacion': publicacion,
        'cambio': cambio,
        'razon': razon,
        'from_email':from_email
    })

    if email_content:
        email = EmailMessage(subject, email_content, from_email, recipient_list)
        email.content_subtype = "html"
        email.send()
        print("Notificación enviada")
