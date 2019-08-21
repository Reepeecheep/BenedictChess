from django.contrib import admin
from Apps.match.models import Match, Match_Move

# Register your models here.
admin.site.register(Match)
admin.site.register(Match_Move)