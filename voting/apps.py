
from django.apps import AppConfig


class VotingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voting'
    label: str = "voting"


        