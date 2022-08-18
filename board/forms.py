from django import forms
from .models import Board, Comment




class CommentForm(forms.ModelForm):
  body = forms.CharField(label="",  widget=forms.TextInput(attrs={'placeholder':'Write a comment','size':30}), required=True)
  
  class Meta:
    model = Comment
    fields = ['body',]
    
    
    
    
class BoardImageUpdate(forms.ModelForm):
  
  class Meta:
    model = Board
    fields = ['image']
    
    
    
    
class BoardInfoUpdate(forms.ModelForm):
  
  class Meta:
    model = Board
    fields = ['description']