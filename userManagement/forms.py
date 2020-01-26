from django import forms
from security.models import User


class notificationUpdateForm(forms.ModelForm):
    receivesAlerts = forms.BooleanField(required=False, label='Receive alerts')

    class Meta:
        model = User
        fields = ['receivesAlerts']

