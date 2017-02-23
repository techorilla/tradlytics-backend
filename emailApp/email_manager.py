import os
from datetime import datetime as dt

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage

from doniServer.celery import app
from emailApp.models import *

common_email_images = [
        'blog-background.jpg',
        'logo.png',
        'facebook.png',
        'linkedin.png',
        'twitter.png',
    ]


@app.task
def send_email(template_name, context, subject, send_to_email=['immadimtiaz1990@gmail.com']):
    from_email = 'Doni & Company <%s>' % settings.EMAIL_HOST_USER
    print from_email
    email = EmailMessage.objects.get(name=template_name)
    base_template = email.base_template.template
    body = email.body
    msg = base_template.replace('%year', str(dt.today().year))
    msg = msg.replace('%body', body)

    for (cont, value) in context.items():
        print (cont, value)
        msg = msg.replace(str('%') + cont, value)

    message = EmailMultiAlternatives(subject, msg, from_email, send_to_email)
    message.attach_alternative(msg, 'text/html')

    # Attaching Icons and logos just add the image file name in the array below
    for f in common_email_images:
        fp = open(os.path.join(settings.EMAIL_ASSETS, f), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<{}>'.format(f))
        message.attach(msg_img)

    return message.send()


