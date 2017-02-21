from django.conf import settings
from datetime import datetime as dt
from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage
import os


class EmailManager(object):

    def send_newsletter_email(self):
        return None

    def send_contact_us_email(self, name, subject, email_message, from_email, send_to_email):

        images = [
            'blog-background.jpg',
            'logo.png',
            'facebook.png',
            'linkedin.png',
            'twitter.png',
        ]

        with open(settings.CONTACT_US_EMAIL_TEMPLATE, 'r') as f:
            email_template = f.read()
            msg = email_template.replace('%year', str(dt.today().year)).replace('%name', name)
            message = EmailMultiAlternatives(subject, msg, from_email, send_to_email)
            message.attach_alternative(msg, 'text/html')
            # Attaching Icons and logos just add the image file name in the array below
            for f in images:
                fp = open(os.path.join(settings.EMAIL_ASSETS, f), 'rb')
                msg_img = MIMEImage(fp.read())
                fp.close()
                msg_img.add_header('Content-ID', '<{}>'.format(f))
                message.attach(msg_img)
        return message.send()