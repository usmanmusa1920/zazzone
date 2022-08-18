from django.db import models
from django.utils import timezone
from  django.urls import reverse

from django.conf import settings
User = settings.AUTH_USER_MODEL



class Board(models.Model):
  owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='board_owner')
  followers = models.ManyToManyField(User, blank=True, related_name='followers')
  description = models.TextField(blank=True, null=True)
  image = models.ImageField(default='board_default_img.jpg', upload_to='users_board_pic')
  timestamp = models.DateTimeField(default=timezone.now)
  
  def __str__(self):
    return f'{self.owner.first_name} {self.owner.last_name} ({self.owner}) board, created on {self.timestamp}'
  
  
  
  
class Post(models.Model):
  publisher = models.ForeignKey(Board, on_delete=models.CASCADE)
  pub_date = models.DateTimeField(default=timezone.now)
  last_modified = models.DateTimeField(auto_now=True)
  title = models.CharField(max_length=255, blank=True, null=True)
  image = models.ImageField(blank=True, null=True, upload_to='board_post_pic')
  text = models.TextField(blank=True, null=True,)
  code = models.TextField(blank=True, null=True)
  likers = models.ManyToManyField(User, blank=True, related_name='board_post_likers')
  
  def __str__(self):
    return 'Post number ' + str(self.id) + ' by ' + str(self.publisher) + ' on ' + str(self.pub_date)
  
  def get_absolute_url(self):
      return reverse("board:Board_Detail", kwargs={"pk": self.pk, "username": self.publisher})
    
    
    
    
class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='board_commentator')
  com_date = models.DateTimeField(auto_now_add=True)
  body = models.TextField()
  
  def __str__(self):
    return 'Commnt by {} on {}'.format(self.commentator, self.com_date)