import logging
import uuid
import os

from django.template.loader import render_to_string 
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as gettext
from django.core.mail import send_mail, send_mass_mail, EmailMessage

from voting.config import *

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        user_model = get_user_model()
        log = logging.getLogger('voting')

        if not user_model.objects.filter(username="admin").first():
            log.info("Creating default superuser with user and password: admin")
            password = str(uuid.uuid4())
            user_model.objects.create_superuser('admin', ADMIN_MAIL, password)
            email = EmailMessage(
                "Credenziali amministrazione per il voto ",
                render_to_string('email/admin-credentials.txt', {
                    "id": password,
                    "host": HOST_NAME
                }),
                'abruzzo@mensa.it',
                [ADMIN_MAIL],
                ['votazionimensaitalia@gmail.com'],
            )
            email.send()
            