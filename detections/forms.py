from django import forms

from detections.models import SentinelIdentity, MacIdentity


class DetectionFilterForm(forms.Form):
    sentinel = forms.ModelMultipleChoiceField(queryset = None)
    sender = forms.ModelMultipleChoiceField(queryset = None)
    receiver = forms.ModelMultipleChoiceField(queryset = None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DetectionFilterForm, self).__init__(*args, **kwargs)
        self.fields['sentinel'] = forms.ModelMultipleChoiceField(queryset = SentinelIdentity.objects.filter(user = user))
        self.fields['sender'] = forms.ModelMultipleChoiceField(queryset = MacIdentity.objects.filter(user = user))
        self.fields['receiver'] = forms.ModelMultipleChoiceField(queryset = MacIdentity.objects.filter(user = user))
