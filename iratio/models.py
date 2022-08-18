from django.db import models
from django.utils import timezone

from django.conf import settings
User = settings.AUTH_USER_MODEL


class Iratio(models.Model):
  solver = models.ForeignKey(User, on_delete=models.CASCADE)
  pub_date = models.DateTimeField(default=timezone.now)
  first = models.FloatField(blank=True, null=True)
  second = models.FloatField(blank=True, null=True)
  operator_choice = [('add', 'Add'), ('subtract', 'Subtract'), ('multiply', 'Multiply'), ('divide', 'Divide')]
  operator = models.CharField(max_length=100, default='add', choices=operator_choice)
  result = models.FloatField(blank=True, null=True)
  
  def __str__(self):
    return f'{self.solver}\'s iRatio number {self.id}'