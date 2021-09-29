from django.db import models

# Create your models here.


class Vote(models.Model):
    voteKey = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    candidate = models.CharField(max_length=100)
    vote = models.CharField(max_length=100)

    class Meta:
        unique_together=["voteKey", "category", "candidate"]

class Voter(models.Model):
    emailKey = models.CharField(max_length=100, primary_key=True)
    hasVoted = models.BooleanField()

