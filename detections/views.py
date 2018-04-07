from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from detections.models import Detection, MacIdentity, SentinelIdentity


class MacIdentities(ListView):
    context_object_name = 'mac_identities_list'

    def get_queryset(self):
        queryset = MacIdentity.objects.filter(user=self.request.user)
        return queryset


class Detections(ListView):
    context_object_name = 'detection_list'
    template_name = 'detections/detections.html'

    def get_queryset(self):
        queryset = Detection.objects.filter(user=self.request.user)
        return queryset



def report(request, det):
    detections = []
    user = None
    for detection in det.split(","):
        print(detection)
        (sender, receiver, sentinel, sequence, rssi) = detection.split(";")
        if user is None:
            sentinel_identity = get_object_or_404(SentinelIdentity, mac=sentinel)
        detections.append((sender, receiver, sentinel, sequence, rssi))
    with transaction.atomic():
        for (sender, receiver, sentinel, sequence, rssi) in detections:
            d = Detection.objects.create(sender = sender, receiver = receiver, sentinel = sentinel,
                                         sentinel_identity=sentinel_identity, sequence = sequence,
                                         rssi = rssi)
            d.save()
    return HttpResponse(status=200)

class MacIdentityCreate(CreateView):
    model = MacIdentity
    fields = ['mac', 'name']
    success_url = '/mac_identities/'

class MacIdentityUpdate(UpdateView):
    model = MacIdentity
    fields = ['mac', 'name']
    success_url = '/mac_identities/'

class MacIdentityDelete(DeleteView):
    model = MacIdentity
    fields = ['mac', 'name']
    success_url = '/mac_identities/'

class SentinelIdentities(ListView):
    context_object_name = 'sentinel_identities_list'

    def get_queryset(self):
        queryset = SentinelIdentity.objects.filter(user=self.request.user)
        return queryset

class SentinelIdentityUpdate(UpdateView):
    model = SentinelIdentity
    fields = ['name']
    success_url = '/sentinel_identities/'

class Detections(ListView):
    context_object_name = 'detection_list'

    def get_queryset(self):
        queryset = Detection.objects.filter(sentinel_identity__user=self.request.user)
        return queryset

class DetectionView(DetailView):
    model = Detection
