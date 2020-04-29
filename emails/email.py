from django.db.models import Max
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse

from itemManagement.models import Photo
from security.models import User
from django.conf import settings

from django.core.signing import Signer

import os


class EmailManager:

    @staticmethod
    def __throwIfEmailIsntConfigured():
        if not settings.EMAIL_CONFIGURED:
            raise "Attempted to send email without an smtp server configured"

    @staticmethod
    def __sendEmail(to, subject, plaintext, html):
        EmailManager.__throwIfEmailIsntConfigured()
        if isinstance(to, str):
            to = [to]
        send_mail(
            subject=subject,
            message=plaintext,
            from_email=settings.EMAIL_FROM,
            recipient_list=to,
            html_message=html,
            fail_silently=False,
        )

    @staticmethod
    def sendAlertEmails(items):
        EmailManager.__throwIfEmailIsntConfigured()
        emails = list(map(lambda x: x.email, User.objects.filter(receivesAlerts=True, is_superuser=True)))
        signer = Signer(sep='?')
        if len(emails) == 0 or len(items) == 0:
            return
        missingImage = f"https://{os.environ['DOMAIN']}/static/itemManagement/default_image.svg"
        items = list(map(lambda item: {'name': item.title,
                                       "unit": item.unit,
                                       "level": item.totalQuantity,
                                       "par": item.alertThreshold,
                                       "image": missingImage \
                                           if ((image := item.photo_set.first()) is None) \
                                           else \
                                           signer.sign(f"https://{os.environ['DOMAIN']}{reverse('get-photo', args=(image.id,))}"),
                                       "link": f"https://{os.environ['DOMAIN']}{reverse('item-details', args=(item.id,))}"
                                       }, items))
        icon = f"https://{os.environ['DOMAIN']}/static/itemManagement/crest.png"
        args = {"items": items, "icon": icon}
        html = render_to_string('alert.html', args)
        plain = render_to_string('alert.plaintext', args)
        EmailManager.__sendEmail(to=emails, subject=f"Inventory Level Alert: {len(items)} are below par", plaintext=plain, html=html)

    @staticmethod
    def sendPasswordResetEmail(user, token, uidb64):
        EmailManager.__throwIfEmailIsntConfigured()
        icon = f"https://{os.environ['DOMAIN']}/static/itemManagement/crest.png"
        link = f"https://{os.environ['DOMAIN']}{reverse('user-register', args=(uidb64, token,))}"
        args = {"link": link, "icon": icon}
        html = render_to_string('reset.html', args)
        plain = render_to_string('reset.plaintext', args)
        EmailManager.__sendEmail(to=user.email, subject=f"Patient Simulation Lab Inventory Password Reset Request", plaintext=plain, html=html)

    @staticmethod
    def sendAccountSetupEmail(user, token, uidb64):
        EmailManager.__throwIfEmailIsntConfigured()
        icon = f"https://{os.environ['DOMAIN']}/static/itemManagement/crest.png"
        link = f"https://{os.environ['DOMAIN']}{reverse('user-register', args=(uidb64, token,))}"
        args = {"link": link, "icon": icon}
        html = render_to_string('newAccount.html', args)
        plain = render_to_string('newAccount.plaintext', args)
        EmailManager.__sendEmail(to=user.email, subject=f"Patient Simulation Lab Inventory Account Creation", plaintext=plain, html=html)
