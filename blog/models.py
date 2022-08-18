from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.conf import settings
User = settings.AUTH_USER_MODEL


class Post(models.Model):
  publisher = models.ForeignKey(User, on_delete=models.CASCADE)
  pub_date = models.DateTimeField(default=timezone.now)
  last_modified = models.DateTimeField(auto_now=True)
  title = models.CharField(max_length=255, blank=True, null=True)
  image = models.ImageField(blank=True, null=True, upload_to='blog_post_pic')
  text = models.TextField(blank=True, null=True,)
  code = models.TextField(blank=True, null=True)
  likers = models.ManyToManyField(User, blank=True, related_name='likers')
  
  def __str__(self):
    return 'Post number ' + str(self.id) + ' by ' + str(self.publisher) + ' on ' + str(self.pub_date)
  
  def get_absolute_url(self):
      return reverse("Blog_Detail", kwargs={"pk": self.pk})
    
    
    
class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  commentator = models.ForeignKey(User, on_delete=models.CASCADE)
  com_date = models.DateTimeField(auto_now_add=True)
  body = models.TextField()
  
  def __str__(self):
    return 'Commnt by {} on {}'.format(self.commentator, self.com_date)