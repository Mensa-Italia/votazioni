import logging
import uuid
import os

from django.template.loader import render_to_string 
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as gettext
from django.core.mail import send_mail, send_mass_mail, EmailMessage

from voting.config import *
from voting.models import *

class Command(BaseCommand):
    help = 'gets stats'

    def handle(self, *args, **options):
        v = Voter.objects.count()
        print('votes:', v)
        