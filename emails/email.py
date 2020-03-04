from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from security.models import User
from django.conf import settings

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
    def sendAlertEmails(item):
        EmailManager.__throwIfEmailIsntConfigured()
        emails = list(map(lambda x: x.email, User.objects.filter(receivesAlerts=True)))
        if len(emails) == 0:
            return
        args = {'name': item.title,
                "unit": item.unit,
                "level": item.totalQuantity,
                "par": item.alertThreshold,
                "link": f"https://{os.environ['DOMAIN']}{reverse('item-details', args=(item.id,))}"
                }
        html = render_to_string('alert.html', args)
        plain = render_to_string('alert.plaintext', args)
        EmailManager.__sendEmail(to=emails, subject=f"Inventory Level Alert: {item.title}", plaintext=plain, html=html)

    @staticmethod
    def sendPasswordResetEmail(user, token, uidb64):
        EmailManager.__throwIfEmailIsntConfigured()
        args = {"link": f"https://{os.environ['DOMAIN']}{reverse('forget-password-confirm', args=(uidb64, token,))}"}
        html = render_to_string('reset.html', args)
        plain = render_to_string('reset.plaintext', args)
        EmailManager.__sendEmail(to=user.email, subject=f"Patient Simulation Lab Inventory Password Reset Request", plaintext=plain, html=html)


    @staticmethod
    def sendAccountSetupEmail(user, token, uidb64):
        EmailManager.__throwIfEmailIsntConfigured()
        args = {"link": f"https://{os.environ['DOMAIN']}{reverse('user-register', args=(uidb64, token,))}"}
        html = render_to_string('newAccount.html', args)
        plain = render_to_string('newAccount.plaintext', args)
        EmailManager.__sendEmail(to=user.email, subject=f"Patient Simulation Lab Inventory Account Creation", plaintext=plain, html=html)
