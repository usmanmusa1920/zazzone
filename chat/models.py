from django.db import models
from django.utils import timezone
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Message(models.Model):
    from_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_sender')
    to_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_receiver')

    message = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='chat_chat_pic')
    timestamp = models.DateTimeField(default=timezone.now)

    # This  is_msg_added, we use it to mate our filter well organize, it didn't do anything else apart from that
    is_msg_added = models.BooleanField(default=False)

    # This is_new_message, we use it to see if the sender of a message, send another additional message, before he/she get reply from who he/she sent a message to
    is_new_message = models.BooleanField(default=False)

    # At this we filter to see if a user reply a message, before the user that sent him/her a message send another one again
    is_msg_replied = models.BooleanField(default=False)

    # This one it let us know if a message is seen
    is_view = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Message send from {self.from_sender} to {self.to_receiver} on {self.timestamp} ({self.message})'
