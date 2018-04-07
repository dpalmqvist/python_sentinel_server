from django.contrib import admin

# Register your models here.
from detections.models import Detection, MacIdentity, SentinelIdentity

admin.site.register(Detection)
admin.site.register(MacIdentity)
admin.site.register(SentinelIdentity)