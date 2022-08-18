from django.db import models
from django.utils import timezone


from django.contrib.auth import get_user_model
User = get_user_model()




class Zone(models.Model):
  name = models.CharField(max_length=255)
  creator = models.ForeignKey(User, models.SET_NULL, default=None, blank=True, null=True)
  members = models.ManyToManyField(User, blank=True, related_name='members')
  
  zone_choices= [('business', 'Business'), ('public', 'Public'), ('school', 'School'), ('family', 'Family'), ('other','Other')]
  custom_zone_type = models.CharField(max_length=255, blank=True, null=True)
  
  # This model field is for zone type if the suggested ones (business, public, school, or family zone is not adorable to a user, then he/she can give a custom zone type type he/she is trying to create)
  zone_type = models.CharField(max_length=100, default='public', choices=zone_choices)
  
  description = models.TextField(blank=True, null=True)
  image = models.ImageField(default='zone_default_img.jpg', upload_to='users_zone_pic')
  timestamp = models.DateTimeField(default=timezone.now)
  
  def __str__(self):
    return f'{self.creator}\'s {self.name} zone, created on {self.timestamp}'
  
  
  
  
class Message(models.Model):
  zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
  zone_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zone_sender')
  message = models.TextField(blank=True, null=True)
  image = models.ImageField(blank=True, null=True, upload_to='zone_chat_pic')
  timestamp = models.DateTimeField(default=timezone.now)
  is_read = models.BooleanField(default=False)
  # you_view = models.ManyToManyField(User, blank=True, related_name='members')
  
  def __str__(self):
    return f'Message from {self.zone_sender} in "{self.zone.name}" zone, on {self.timestamp}'