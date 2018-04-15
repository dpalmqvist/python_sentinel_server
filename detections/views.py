from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView

from detections.models import Detection, MacIdentity, SentinelIdentity

class MacIdentities(LoginRequiredMixin, ListView):
    context_object_name = 'mac_identities_list'

    def get_queryset(self):
        queryset = MacIdentity.objects.filter(user=self.request.user)
        return queryset

@login_required
def detections(request):
    mac_identities = MacIdentity.objects.filter(user=request.user)
    mac_to_name = {}
    for mac_identity in mac_identities:
        mac_to_name[mac_identity.mac] = mac_identity.name
    detections = Detection.objects.filter(sentinel_identity__user=request.user)\
                    .filter(timestamp__gt=datetime.now()-timedelta(days=1))\
                     .order_by('-timestamp')
    detection_list = []
    for detection in detections:
        detection_list.append({"id":detection.id, "timestamp":detection.timestamp,
                               "sender": mac_to_name.get(detection.sender, detection.sender),
                               "receiver":mac_to_name.get(detection.receiver, detection.receiver)})

    template = loader.get_template('detections/detection_list.html')
    context = {'detection_list': detection_list}
    return HttpResponse(template.render(context, request))

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

class MacIdentityCreate(LoginRequiredMixin, CreateView):
    model = MacIdentity
    fields = ['mac', 'name']
    success_url = '/mac_identities/'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(MacIdentityCreate, self).form_valid(form)

class MacIdentityUpdate(LoginRequiredMixin, UpdateView):
    model = MacIdentity
    fields = ['mac', 'name']
    success_url = '/mac_identities/'

class MacIdentityDelete(LoginRequiredMixin, DeleteView):
    model = MacIdentity
    fields = ['mac', 'name']
    success_url = '/mac_identities/'

class SentinelIdentities(LoginRequiredMixin, ListView):
    context_object_name = 'sentinel_identities_list'

    def get_queryset(self):
        queryset = SentinelIdentity.objects.filter(user=self.request.user)
        return queryset

class SentinelIdentityUpdate(LoginRequiredMixin, UpdateView):
    model = SentinelIdentity
    fields = ['name']
    success_url = '/sentinel_identities/'

class Detections(LoginRequiredMixin, ListView):
    context_object_name = 'detection_list'

    def get_queryset(self):
        queryset = Detection.objects.filter(sentinel_identity__user=self.request.user)
        return queryset

class DetectionView(LoginRequiredMixin, DetailView):
    model = Detection
