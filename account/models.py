from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
# from PIL import Image

from django.conf import settings
User = settings.AUTH_USER_MODEL


class UserAccountManager(BaseUserManager):
  def create_user(self, first_name, last_name, username, email, phone_number, password=None):
    if not first_name:
      raise ValueError('Your first name is required')
    if not last_name:
      raise ValueError('Your last name is required')
    if not username:
      raise ValueError('Your username is required')
    if not email:
      raise ValueError('You must provide your email address')
    if not phone_number:
      raise ValueError('Please include your phone number')
    if not password:
      raise ValueError('You must include password')
    
    user = self.model(
      first_name = first_name,
      last_name = last_name,
      username = username,
      email = self.normalize_email(email),
      phone_number = phone_number,
    )
    
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def account_verified(self, first_name, last_name, username, email, phone_number, password):
    user = self.create_user(
      first_name = first_name,
      last_name = last_name,
      username = username,
      email = self.normalize_email(email),
      phone_number = phone_number,
      password = password,
    )
    
    user.save(using=self._db)
    return user
  
  def create_staffuser(self, first_name, last_name, username, email, phone_number, password):
    user = self.create_user(
      first_name = first_name,
      last_name = last_name,
      username = username,
      email = self.normalize_email(email),
      phone_number = phone_number,
      password = password,
    )
    
    user.is_staff = True
    user.save(using=self._db)
    return user
  
  def create_adminuser(self, first_name, last_name, username, email, phone_number, password=None):
    user = self.create_user(
      first_name = first_name,
      last_name = last_name,
      username = username,
      email = self.normalize_email(email),
      phone_number = phone_number,
      password = password,
    )
    
    user.is_staff = True
    user.is_admin = True
    user.save(using=self._db)
    return user
  
  def create_superuser(self, first_name, last_name, username, email, phone_number, password=None):
    user = self.create_user(
      first_name = first_name,
      last_name = last_name,
      username = username,
      email = self.normalize_email(email),
      phone_number = phone_number,
      password = password,
    )
    
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save(using=self._db)
    return user
  
  
  
class UserAccount(AbstractBaseUser):
  first_name = models.CharField(max_length=100, unique=False)
  last_name = models.CharField(max_length=100, unique=False)
  GENDER_CHOICES = [('female', 'Female'), ('male', 'Male'),]
  gender = models.CharField(max_length=100, default='male', choices=GENDER_CHOICES)
  date_of_birth = models.DateField(max_length=100, blank=True, null=True)
  username = models.CharField(max_length=255, unique=True)
  email = models.EmailField(max_length=255, unique=False)
  phone_number = PhoneNumberField(max_length=100, unique=True)
  country = CountryField(max_length=100, blank_label='Select your country',)
  date_joined = models.DateTimeField(default=timezone.now)
  friends = models.ManyToManyField('UserAccount', blank=True)
  
  image = models.ImageField(default='user.png', upload_to='users_profile_pics')
  
  # def save(self, *args, **kwargs):
  #   super().save(*args, **kwargs)
  #   img = Image.open(self.image.path)
  #   if img.height > 250 or img.width > 250:
  #     pic_size = (250, 250)
  #     img.thumbnail(pic_size)
  #     img.save(self.image.path)
      
  is_active = models.BooleanField(default=True)
  is_verified = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  
  # Some additional account encryption (privacy)
  is_num_encrypt = models.BooleanField(default=False)
  is_email_encrypt = models.BooleanField(default=False)
  is_dob_encrypt = models.BooleanField(default=False)
  is_study_status = models.BooleanField(default=False)
  
  objects = UserAccountManager()
  
  USERNAME_FIELD = 'phone_number'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'email']
  
  def __str__(self):
    return self.username
  
  def has_perm(self, perm, obj=None):
    return True
  
  def has_module_perms(self, app_label):
    return True
  
  
  
"""
  Whenever you use blank=True and null=True in a models.py field, make sure you replace it with required=False in forms.py field or in html file.
"""
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(blank=True, null=True)
  institution = models.CharField(max_length=255, blank=True, null=True)
  banner = models.ImageField(default='user_banner_default.jpg', upload_to='users_profile_banner')
  
  def __str__(self):
    return f'{self.user.username}\'s profile'
  
  
  
class FriendRequest(models.Model):
  sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
  receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
  time = models.DateTimeField(default=timezone.now)
  
  def __str__(self):
    return f'{self.sender} send friend request to {self.receiver}'
  
  
  
class MessageUs(models.Model):
  full_name = models.CharField(max_length=255, blank=False, null=False)
  email = models.CharField(max_length=255, blank=False, null=False)
  text_body = models.TextField(blank=False, null=False)
  timestamp = models.DateTimeField(default=timezone.now)
  is_read = models.BooleanField(default=False)
  is_client = models.BooleanField(default=False)
  
  def __str__(self):
    return 'Message sent from {} on {}'.format(self.email, self.timestamp)