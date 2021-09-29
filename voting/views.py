import os
import io
import json
import uuid
import datetime

from django.shortcuts import render
from django.template.loader import render_to_string 
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django import forms

import pandas as pd

from .models import * 
from .config import *

conf = json.load(open('conf.json'))
from_date = datetime.datetime.strptime(conf['voting_begin'], "%Y-%m-%dT%H:%M:%S")
to_date = datetime.datetime.strptime(conf['voting_end'], "%Y-%m-%dT%H:%M:%S")

@login_required
def mgmt(request):
    if request.user.is_superuser:
        return render(request, 'mgmt-menu.html', {
            "actions": [
                {"name": "Carica utenti", "url": "/management/upload"},
                {"name": "Invia chiavi di accesso", "url": "/management/send"},
                {"name": "Statistiche", "url": "/management/stats"},
            ]
        })
    else:
        return render(request, 'error.html', {'error': 'Utenza senza diritti sufficienti'})


class UploadFileForm(forms.Form):
    file = forms.FileField()

def handle_uploaded_file(fff):
    ff = pd.read_excel(io.BytesIO(fff.read()))
    for v in conf['input'].get('valid', []):
        ff = ff[ff[v['col']] == v['val']]
    ff = ff.rename(columns=conf['input']['columns'])
    ff = ff[conf['input']['columns'].values()]
    print(ff)


    ff['uuid'] = ff.apply(lambda _: str(uuid.uuid4()), axis=1)
    ff.to_csv('local.csv')
    
@login_required
def mgmt_upload(request):
    if request.user.is_superuser:
        form = None
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                #try:
                    handle_uploaded_file(request.FILES['file'])
                    return HttpResponseRedirect('/management/send')
                #except Exception as ex:
                #    return render(request, 'error.html', {'error': str(ex)})
        else:
            form = UploadFileForm()
        return render(request, 'mgmt-upload.html', {'form': form})
    else:
        return render(request, 'error.html', {'error': 'Utenza senza diritti sufficienti'})

@login_required
def mgmt_send(request):
    if request.user.is_superuser:
        if request.method == "GET":
            if os.path.exists('local.csv'):
                rows = pd.read_csv('local.csv')
                rows = rows.sort_values(by=['name','surname'])
                rrows = json.loads(rows.to_json(orient="records"))
                return render(request, 'mgmt-sendkeys.html', {'items': rrows})
            else:
                return render(request, 'error.html', {'error': 'file aventi diritto non caricato correttamente'})
        else:
            to_send = request.POST.getlist('send')
            rows = pd.read_csv('local.csv')
            for email in to_send:
                row = rows[rows['email']==email].iloc[0]
                gemail = EmailMessage(
                    conf.get('voting_title'),
                    'id: {}'.format(row.uuid),
                    'votazioni@mensa.it',
                    [email],
                    ['votazionimensaitalia@gmail.com'],
                )
                gemail.send()
            return render(request, 'sent.html', {"sent": len(to_send)})
        #send mails
    else:
        return render(request, 'error.html', {'error': 'Utenza senza diritti sufficienti'})




@login_required
def mgmt_stats(request):
    if request.user.is_superuser:
        if request.method == "GET":
            if os.path.exists('local.csv'):
                rows = pd.read_csv('local.csv')
                rrows = len(json.loads(rows.to_json(orient="records")))
                voters = Voter.objects.all().count()
                votes = Vote.objects.all().count()
                votes_tot = 3
                return render(request, 'mgmt-stats.html', {
                    'voting': conf,
                    'votes': votes,
                    'voters': voters,
                    'items': rrows
                })
            else:
                return render(request, 'error.html', {'error': 'file aventi diritto non caricato correttamente'})
    else:
        return render(request, 'error.html', {'error': 'Utenza senza diritti sufficienti'})


def vote(request):
    now = datetime.datetime.now()
    rows = pd.read_csv('local.csv')
    votingkey = request.GET.get('key')
    row = rows[rows['uuid']==votingkey]
    if request.method == "GET":
        if row.shape[0] == 1:
            print(row)
            row = row.iloc[0]
            if now > from_date and now < to_date:
                mode = conf.get('mode')
                if mode in [1,2,3,4]:
                    return render(request, 'vote.html', {'voting': conf})
            else:
                return render(request, 'error.html', {'error': 'Accesso in corso fuori dal periodo di voto'})

        else:
            return render(request, 'error.html', {'error': 'Chiave di voto non valida'})
    else:
        print(row)
        row = row.iloc[0]
        vote_id = str(uuid.uuid4())
        vr = Voter()
        vr.emailKey = votingkey
        vr.hasVoted = True
        vr.save()
        for p in request.POST.keys():
            if 'csrf' not in p:
                pk = request.POST[p].split(':')
                v = Vote()
                v.voteKey = vote_id
                v.candidate = pk[0]
                v.category = pk[1]
                v.vote = "1"
                v.save()

        gemail = EmailMessage(
            "Grazie per aver votato ",
            'id: {}'.format(vote_id),
            'votazioni@mensa.it',
            [row.email],
            ['votazionimensaitalia@gmail.com'],
        )
        gemail.send()
        #send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)
        return render(request, 'voted.html', {'key':vote_id})

def verify(request):
    votingkey = request.GET.get('key')
    now = datetime.datetime.now()
    if Vote.objects.filter(voteKey=votingkey).count() > 0:
        t_params = {}
        myvotes = Vote.objects.filter(voteKey=votingkey).count()
        t_params['myvotes'] = myvotes
        if now > voting_end:
            t_params['mode'] = 'full'
            rows = pd.read_csv('local.csv')
            rrows = len(json.loads(rows.to_json(orient="records")))
            voters = Voter.objects.all().count()
            votes = Vote.objects.all().count()
            t_params['voting'] = conf
            t_params['votes'] = votes
            t_params['voters'] = voters
            t_params['items'] = rrows
        return render(request, 'verify.html', t_params)
    else: 
        return render(request, 'error.html', {'error': 'chiave di voto non presente nel sistema'})

