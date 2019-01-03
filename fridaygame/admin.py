from django.contrib import admin
from fridaygame import models as fg_models

admin.site.register(fg_models.User)
admin.site.register(fg_models.Game)
admin.site.register(fg_models.Team)
admin.site.register(fg_models.Vote)
