from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import Profile, MessageUs


from django.contrib.auth import get_user_model
User = get_user_model()



class SignupForm(UserCreationForm):
  GENDER_CHOICES = [('female', 'Female'), ('male', 'Male'),]
  gender = forms.ChoiceField(label="", choices=GENDER_CHOICES, widget=forms.RadioSelect())
  
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'username', 'email', 'phone_number', 'country', 'password1', 'password2']
    widgets = {'country': CountrySelectWidget()}
    
    
    
class UserUpdate(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email', 'is_study_status']
    
    
class PrivacyPage(forms.ModelForm):
  
  class Meta:
    model = User
    fields = ['is_num_encrypt', 'is_email_encrypt', 'is_dob_encrypt']
    
    
    
class ImageUpdate(forms.ModelForm):
  class Meta:
    model = User
    fields = ['image']
    
    
    
class ProfileUpdate(forms.ModelForm):
  bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Add your bio here!','size':40}),required=False)
  institution = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Add your collage here!','size':40}))
  
  class Meta:
    model = Profile
    fields = ['bio', 'institution']
    
    
    
class BannerUpdate(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['banner']
    
    
    
class PasswordChange(PasswordChangeForm):
  class Meta:
    model = User
    
    
    
class MessageUsForm(forms.ModelForm):
  class Meta:
    model = MessageUs
    fields = ['full_name', 'email', 'text_body', 'is_client']