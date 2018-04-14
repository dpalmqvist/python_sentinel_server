from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.
from detections.models import Detection, MacIdentity

def main(request):
    if request.user.is_authenticated:
        mac_identities = MacIdentity.objects.filter(user=request.user)
        mac_to_name = {}
        for mac_identity in mac_identities:
            mac_to_name[mac_identity.mac] = mac_identity.name

        detections = Detection.objects.filter(sentinel_identity__user=request.user).order_by('-timestamp')[:10]
        detection_list = []
        for detection in detections:
            detection_list.append({"id":detection.id, "timestamp":detection.timestamp,
                               "sender": mac_to_name.get(detection.sender, detection.sender),
                               "receiver":mac_to_name.get(detection.receiver, detection.receiver)})

        context = {
            'mac_identities': mac_identities,
            'detection_list': detection_list,
        }
    else:
        context = {}
    template = loader.get_template('main/main.html')
    return HttpResponse(template.render(context, request))

