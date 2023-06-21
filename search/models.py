from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_to_search = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.user} search for {self.data_to_search}'
