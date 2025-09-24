import logging
import uuid
import os

from django.template.loader import render_to_string 
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as gettext
from django.core.mail import send_mail, send_mass_mail, EmailMessage

import pandas as pd

import json

from voting.config import *

class Command(BaseCommand):
    help = 'Send all mail'

    def handle(self, *args, **options):
        conf = json.load(open('conf.json'))
        rows = pd.read_csv('local.csv')
        sent = []
        if os.path.exists('sent.json'):
            with open('sent.json') as sent_file:
                sent = json.load(sent_file)
        for row in rows.itertuples(index=True, name="Pandas"):
            if row.email not in sent:
                print('sending', row.email)
                gemail = EmailMessage(
                    conf.get('voting_title'),
                    render_to_string('email/voting-credentials.txt', {"emailKey":row.uuid, "name": row.name, "surname": row.surname}),
                    'votazioni@mensa.it',
                    [row.email],
                    ['votazionimensaitalia@gmail.com'],
                )
                gemail.send()
                print('sent', row.email)
                sent.append(row.email)
                with open('sent.json', 'w+') as sent_file:
                    json.dump(sent, sent_file)
            else: 
                print('already sent', row.email)