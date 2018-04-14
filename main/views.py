from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.
from detections.models import Detection, MacIdentity

def main(request):
    if request.user.is_authenticated:
        mac_identities = MacIdentity.objects.filter(user = request.user)
        detections = Detection.objects.filter(sentinel_identity__user = request.user)[:10]
        context = {
            'mac_identities': mac_identities,
            'detections': detections,
        }
    else:
        context = {}
    template = loader.get_template('main/main.html')
    return HttpResponse(template.render(context, request))

