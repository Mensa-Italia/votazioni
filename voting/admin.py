from django.contrib import admin

from .models import * 

# Register your models here.

class VoteAdmin(admin.ModelAdmin):
    list_display  = ( 'voteKey', 'category', 'candidate', 'vote')


class VoterAdmin(admin.ModelAdmin):
    list_display  = ('emailKey', 'hasVoted')


admin.site.register(Vote, VoteAdmin)
admin.site.register(Voter, VoterAdmin)