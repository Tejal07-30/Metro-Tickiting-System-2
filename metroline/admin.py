from django.contrib import admin
from .models import MetroLine, Station, DailyFootfall

# Register your models here so they show up in the Admin interface.

admin.site.register(MetroLine)
admin.site.register(Station)
admin.site.register(DailyFootfall)