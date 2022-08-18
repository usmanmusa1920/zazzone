from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
  body = forms.CharField(label="",  widget=forms.TextInput(attrs={'placeholder':'Write a comment','size':30}), required=True)
  
  class Meta:
    model = Comment
    fields = ['body',]