from django import forms
from security.models import User
from django.contrib.auth.forms import UserCreationForm


class notificationUpdateForm(forms.ModelForm):
    receivesAlerts = forms.BooleanField(required=False, label='Receive alerts')

    class Meta:
        model = User
        fields = ['receivesAlerts']


class userCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['name', 'password1', 'password2']

class userRoleForm(forms.ModelForm):
    is_superuser = forms.BooleanField(required=False, label='Admin')

    class Meta:
        model = User
        fields = ['is_superuser']