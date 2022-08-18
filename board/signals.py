from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Board

from django.conf import settings
User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_board(sender, instance, created, **kwargs):
  if created:
    Board.objects.create(owner=instance)
    
    
    
@receiver(post_save, sender=User)
def save_board(sender, instance, **kwargs):
  instance.profile.save()