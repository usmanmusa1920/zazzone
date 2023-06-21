from django import forms
from .models import Iratio


class IratioForm(forms.ModelForm):
    operator_choice = [('add', '+'), ('subtract', '-'), ('multiply', '*'), ('divide', '/')]
    # operator = forms.ChoiceField(choices=operator_choice, widget=forms.RadioSelect())
    operator = forms.ChoiceField(choices=operator_choice)
    
    class Meta:
        model = Iratio
        fields = ['first', 'second', 'result', 'operator']
