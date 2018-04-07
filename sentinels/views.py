from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from detections.models import SentinelIdentity
from sentinels.forms import ClaimSentinelForm

@login_required()
def claim_sentinel(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = ClaimSentinelForm(request.POST)
        if form.is_valid():
            exists = SentinelIdentity.objects.filter(mac = form.cleaned_data['sentinel_mac_address'])
            if len(exists) == 0:
                s = SentinelIdentity(
                    mac = form.cleaned_data['sentinel_mac_address'],
                    name = form.cleaned_data['name'],
                    user = request.user
                )
                s.save()
                return HttpResponseRedirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClaimSentinelForm()
    template = loader.get_template('sentinels/claim_sentinel.html')
    return HttpResponse(template.render({'form':form}, request))
