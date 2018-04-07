from django import forms

from detections.models import SentinelIdentity


class ClaimSentinelForm(forms.Form):
    sentinel_mac_address = forms.CharField(label='Sentinel mac address', max_length=100)
    name = forms.CharField(label='Name of sentinel', max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        existing = SentinelIdentity.objects.filter(mac = cleaned_data['sentinel_mac_address'])
        if len(existing) > 0:
            raise forms.ValidationError(
                "Mac address is already claimed"
            )