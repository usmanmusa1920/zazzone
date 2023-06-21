from django import forms
from .models import Zone, Message


class ZoneCreatForm(forms.ModelForm):
    zone_choices = [
        ('business', 'Business'), ('public', 'Public'), ('school', 'School'), ('family', 'Family'), ('other', 'Other')]
    zone_type = forms.ChoiceField(label="", choices=zone_choices, widget=forms.RadioSelect())

    class Meta:
        model = Zone
        fields = ['name', 'description', 'custom_zone_type', 'zone_type']


class ZoneUpdateImage(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['image']


class ZoneUpdateInfo(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'description']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message', 'image']
