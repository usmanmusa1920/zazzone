from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms as acc_forms
from .models import FriendRequest, MessageUs
from blog.models import Post
from chat.models import Message
from board.models import Board
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from phonenumbers import carrier, timezone


from django.contrib.auth import get_user_model
User = get_user_model()


import phonenumbers
import os




def about(request):
  messages_all = MessageUs.objects.filter(is_read=False).order_by('-timestamp')
  
  paginator_message = Paginator(messages_all, 10)
  page = request.GET.get('page')
  messages_us = paginator_message.get_page(page)
  
  if request.method == 'POST':
    form = acc_forms.MessageUsForm(request.POST)
    if form.is_valid():
      if request.user.is_authenticated:
        instance = form.save(commit=False)
        instance.is_client = True
        instance.save()
        
        full_name = form.cleaned_data.get('full_name')
        messages.success(request, f'Weldone {full_name}, your message has been sent. We will inbox you in your zazzone account')
        return redirect('about')
      else:
        form.save()
        full_name = form.cleaned_data.get('full_name')
        messages.success(request, f'Weldone {full_name}, your message has been sent. We really appreciate')
        return redirect('about')
  else:
    form = acc_forms.MessageUsForm()
  context = {
    'form':form,
    'messages_us':messages_us,
  }
  return render(request, 'account/about.html', context)


# this will mark message sent to us (to our team) as read
def markMessageUs(request, message_id):
  message_not_read = MessageUs.objects.get(id=message_id)
  if request.user.is_superuser:
    message_not_read.is_read = True
    message_not_read.save()
    return redirect(reverse('about'))
  return False


# this will delete the message sent to us (to our team)
def deleteMessageUs(request, message_id):
  find_match_id = MessageUs.objects.get(id=message_id)
  if request.user.is_superuser:
    find_match_id.delete()
    return redirect(reverse('about'))
  return False



def signupView(request):
  this_year = datetime.today().year
  if request.method == 'POST':
    form = acc_forms.SignupForm(request.POST)
    if form.is_valid():
      form.save()
      first_name = form.cleaned_data.get('first_name')
      last_name = form.cleaned_data.get('last_name')
      messages.success(request, f'Welcome {first_name} {last_name}, your account has been created, you are ready to login!')
      return redirect('login')
  else:
    form = acc_forms.SignupForm()
  context = {
    'form':form,
    'this_year':this_year
  }
  return render(request, 'account/signup.html', context)




@login_required
def sendFriendRequest(request, req_pk):
  # This is the current logged in user who will send the request
  sender = request.user
  # This is the user that will receive the request
  receiver = User.objects.get(id=req_pk)
  """
    We are checking if the receiver is in the current logged in user (sender) friend list, else it will move to the next condition (else)
  """
  if receiver in sender.friends.all():
    messages.success(request, f'You are already a friend with {receiver.first_name} {receiver.last_name}')
    return redirect(reverse('profile_user', kwargs={'username':receiver}))
  else:
    friend_req = FriendRequest.objects.filter(Q(sender=receiver, receiver=sender))
    """
      Here we are checking to see if wheather the current user (sender) have a friend request, which was already sent from the user he is trying to send a friend request to (receiver). By the use of the above variable (friend_req)
    """
    if friend_req:
      messages.success(request, f'{receiver.first_name} already sent you friend request')
      return redirect(reverse('profile_user', kwargs={'username':receiver}))
      
      
    friend_request, created = FriendRequest.objects.get_or_create(sender=sender,receiver=receiver)
    """
      Here we check if the request is sent to the desire destination, else it will fall to the next condition.  By the use of the above variables (friend_request and created)
    """
    if created:
      messages.success(request, f'Friend request sent to {receiver.first_name} {receiver.last_name}')
      return redirect(reverse('profile_user', kwargs={'username':receiver}))
    else:
      messages.success(request, f'You already sent friend request to{receiver.first_name} {receiver.last_name}')
      return redirect(reverse('profile_user', kwargs={'username':receiver}))
  
  
  
  
@login_required
def acceptFriendRequest(request, req_pk):
  friend_request = FriendRequest.objects.get(id=req_pk)
  """
    Here we are trying to find the request id from the above variable (friend_request). And if the receiver of the request is the current user so it will add current user to the friend list of the sender (who send the request), as well as to add the sender (who send the request) to the current user friende list.
  """
  if friend_request.receiver == request.user:
    friend_request.sender.friends.add(friend_request.receiver)
    friend_request.receiver.friends.add(friend_request.sender)
    friend_request.delete()
    messages.success(request, f'You and {friend_request.sender.first_name}  {friend_request.sender.last_name} are now friends')
    return redirect(reverse('profile_user', kwargs={'username':friend_request.sender}))
  
    """
      Here, if the sender of the request is the current user, then it will cancel the request and delete it from our data base.
    """
  elif friend_request.sender == request.user:
    friend_request.delete()
    messages.success(request, f'You cancel friend request,you sent to {friend_request.receiver.first_name}\'')
    return redirect(reverse('profile_user', kwargs={'username':friend_request.receiver}))
  else:
    return False
  
  
  
  
@login_required
def declineRequest(request, req_pk):
  friend_request = FriendRequest.objects.get(id=req_pk)
  """
    At this we filter a request id from the FriendRequest model, and if the current user is the receiver of the request (friend_request.receiver), so it will delete the request from our database, or to say it will decline the request.
  """
  if friend_request.receiver == request.user:
    friend_request.delete()
    messages.success(request, f'You declined {friend_request.sender.first_name}\'s friend request')
    return redirect(reverse('profile_user', kwargs={'username':friend_request.sender}))
  
  
  
  
@login_required
def removeFriend(request, user_pk):
  my_friends = request.user.friends
  user_remove = User.objects.get(id=user_pk)
  
  """
    At this point we check to see if the user we are trying to remove is in the current user friends list, as well if the current user is in the user that we are trying to remove friends list. Else it will fall to the next condition
  """
  if user_remove in my_friends.all() and request.user in user_remove.friends.all():
    my_friends.remove(user_remove)
    user_remove.friends.remove(request.user)
    
    """
      Here it will filter messges where the sender is the current user and the receiver is the current user friend (the user you want to unfriend) as well as if any image/images, and then delete the messages
    """
    for msg in Message.objects.filter(to_receiver=user_remove, from_sender=request.user):
      # At this point it search if the message have an image
      if msg.image:
        r = msg.image.path
        # Here it will search if the file or image is available (exist) in our filesystem of our machine
        if os.path.exists(r):
          os.remove(r)
      msg.delete()
      
    """
      Here it will filter messges where the receiver is the current user and the sender is the current usre friend (the user you want to unfriend) as well as if any image/images, and then delete the messages
    """
    for msg in Message.objects.filter(from_sender=user_remove, to_receiver=request.user):
      # At this point it search if the message have an image
      if msg.image:
        r = msg.image.path
        # Here it will search if the file or image is available (exist) in our filesystem of our machine
        if os.path.exists(r):
          os.remove(r)
      msg.delete()
      
    messages.success(request, f'You removed {user_remove.first_name} {user_remove.last_name} from your friend list')
    return redirect(reverse('Profile', kwargs={'username':request.user}))
  else:
    return False
  
  
  
  
# This UserProfile class is for current login user
class UserProfile(LoginRequiredMixin, ListView):
  model = Post
  template_name = 'account/profile.html'
  context_object_name = 'posts'
  ordering = ['-pub_date']
  paginate_by = 5
  
  def get_context_data(self):
    num_info = phonenumbers.parse(str(self.request.user.phone_number), None)
    ro_number = phonenumbers.parse(str(self.request.user.phone_number), 'RO')
    
    
    # Here it detect the request.user phone number (SIM card) carrie
    carr = carrier.name_for_number(ro_number, 'en')
    # This one arrenge the user phone number in international format
    inter_num = phonenumbers.format_number(num_info, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    # This is the information of the user's carrier timezone
    time_zone_1 = timezone.time_zones_for_number(num_info)
    time_zone_2 = timezone.time_zones_for_geographical_number(num_info)
    
    
    # The below followers variable it get all followers of the current user (board follower)
    # followers = Board.objects.get(owner=self.request.user).followers.all()
    followers = self.request.user.board_owner.followers.all()
    # Current user last follower
    last_follower = self.request.user.board_owner.followers.all().order_by('username').last()
    # Current user friends, which will slice only 7 friends in the current user friends list (set)
    my_friends = self.request.user.friends.all()[:7]
    
    
    context = {
        'carrier': carr,
        'inter_num': inter_num,
        'time_zone_1': time_zone_1,
        'time_zone_2': time_zone_2,
        'followers': followers,
        'last_follower': last_follower,
        'my_friends': my_friends,
    }
    return super().get_context_data(**context)
  
  def get_queryset(self):
    user = get_object_or_404(User, username=self.kwargs.get('username')) # OR user = self.request.user
    
    """
      It check to see if the user is sending the request is the user who published the query set of the post, else it fall to the next condition, which is false
    """
    if self.request.user == user:
      return Post.objects.filter(publisher=user).order_by('-pub_date')
    return False
  
  
  
  
"""
  This viewUserProfile function is for the user we want to view his/her profile (maybe a friend or someone else)
"""
@login_required
def viewUserProfile(request, username):
  # Here we get the user id (the user we want to view his/her profile)
  view_user = User.objects.get(username=username)
  # This will filter view_user friends (his/her friends, i.e only 7 friends)
  view_user_friends = view_user.friends.all()[:7]
  # Here we filter all the blog post of the user (the user we want to view his/her profile)
  post = Post.objects.filter(publisher=view_user).order_by('-pub_date')
  
  
  # It filter request where the sender is the user we are viewing his/her profile and the receiver is the current user who is viewing the profile
  friend_req_to_accept = FriendRequest.objects.filter(sender=view_user, receiver=request.user)
  # It filter request where the receiver is the user we are viewing his profile and the sender is the current user who is viewing the profile
  friend_req_to_cancel = FriendRequest.objects.filter(sender=request.user, receiver=view_user)
  
  # This is the pagination of the user (the user we want to view his/her profile) blog post
  paginator = Paginator(post, 5)
  page = request.GET.get('page')
  posts = paginator.get_page(page)
  
  # This is generating the user (the user we want to view his/her profile) phone number infomation
  num_info = phonenumbers.parse(str(view_user.phone_number), None)
  # This is the international formart of the user (the user we want to view his/her profile) phone number
  inter_num = phonenumbers.format_number(num_info, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    
  # The below followers variable it get all followers of the current user (his/her board follower)
  view_user_followers = Board.objects.get(owner=view_user).followers.all()
  # The usr we want to view his profile (his/her board last follower)
  view_user_last_follower = Board.objects.get(owner=view_user).followers.all().order_by('username').last()
  
  context = {
    'view_user':view_user,
    'view_user_friends':view_user_friends,
    'view_user_followers':view_user_followers,
    'view_user_last_follower':view_user_last_follower,
    'inter_num': inter_num,
    'friend_req_to_accept': friend_req_to_accept,
    'friend_req_to_cancel': friend_req_to_cancel,
    'posts':posts,
  }
  return render(request, 'account/profile_friend.html', context)
  
  
  
  
# This UserGallery class is for current login user
class UserGallery(LoginRequiredMixin, ListView):
  model = Post
  template_name = 'account/gallery.html'
  context_object_name = 'galleries'
  ordering = ['-pub_date']
  paginate_by = 6
  
  def get_queryset(self):
    user = get_object_or_404(User, username=self.kwargs.get('username'))
    
    """
      It check to see if the user is sending the request is the user who posted the query set of the post (image), else it fall to the next condition
    """
    if self.request.user == user:
      return Post.objects.filter(publisher=user).order_by('-pub_date')
    return False
  
  
  
  
"""
  This viewUserGallery function is for the user we want to view his/her profile (maybe a friend or someone else)
"""
@login_required
def viewUserGallery(request, username):
  # Here we get the user id (the user we want to view his/her profile)
  view_user = User.objects.get(username=username)
  
  # Here we filter all the blog post of the user (the user we want to view his/her profile)
  gallery = Post.objects.filter(publisher=view_user).order_by('-pub_date')
  
  # This is the pagination of the user (the user we want to view his/her profile) blog gallery
  paginator = Paginator(gallery, 6)
  page = request.GET.get('page')
  galleries = paginator.get_page(page)
  
  context = {
    'view_user':view_user,
    'galleries':galleries,
    'gallery_count':gallery,
  }
  return render(request, 'account/gallery_user.html', context)
  
  
  
  
"""
  This profileUpdate function it will update the current login user account information, but with an exception of media files such as profile image, profile banner etc.
"""
@login_required
def profileUpdate(request):
  
  """
    Here we check if the request method is POST then it will proceed, else it will return the user to the profile update page together with each fields instance
  """
  if request.method == 'POST':
    
    # For user account (u_form)
    u_form = acc_forms.UserUpdate(request.POST, instance=request.user)
    # For user profile (p_form)
    p_form = acc_forms.ProfileUpdate(request.POST, instance=request.user.profile)
    
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, f'Your account has been updated!')
      return redirect(reverse('Profile', kwargs={'username':request.user}))
  else:
    u_form = acc_forms.UserUpdate(instance=request.user)
    p_form = acc_forms.ProfileUpdate(instance=request.user.profile)
    
  context = {
    'u_form':u_form,
    'p_form':p_form
  }
  return render(request, 'account/profile_update.html', context)




# This imageUpdate function it will update the current login user profile image only
@login_required
def imageUpdate(request):
  
  """
    Here we check if the request method is POST then it will proceed, else it will return the user to the profile image update page together with his current profile image instance (image)
  """
  if request.method == 'POST':
    form = acc_forms.ImageUpdate(request.POST, request.FILES, instance=request.user)
    r = request.user.image.path
    if form.is_valid():
      if r != '/home/usman/Desktop/acode/sakyum/sakyum/media/user.png':
        if os.path.exists(r):
          os.remove(r)
      form.save()
      messages.success(request, f'Your profile image has been updated!')
      return redirect(reverse('Profile', kwargs={'username':request.user}))
  else:
    form = acc_forms.ImageUpdate(instance=request.user)
    
  context = {
    'form': form,
  }
  return render(request, 'account/profile_img_update.html', context)




# This bannerUpdate function it will update the current login user profile banner only
@login_required
def bannerUpdate(request):
  """
    Here we check if the request method is POST then it will proceed, else it will return the user to the profile banner update page together with his current profile banner image instance (image)
  """
  if request.method == 'POST':
    form = acc_forms.BannerUpdate(request.POST, request.FILES, instance=request.user.profile)
    r = request.user.profile.banner.path
    if form.is_valid():
      if r != '/home/usman/Desktop/acode/sakyum/sakyum/media/user_banner_default.jpg':
        if os.path.exists(r):
          os.remove(r)
      form.save()
      messages.success(request, f'Your banner image has been updated!')
      return redirect(reverse('Profile', kwargs={'username':request.user}))
  else:
    form = acc_forms.BannerUpdate(instance=request.user.profile)
    
  context = {
    'form': form,
  }
  return render(request, 'account/profile_banner_update.html', context)




# This privacy function that will allow user to hide or unhide some iformation of his account
@login_required
def privacyMe(request):
  # Here we check if the request method is POST then it will proceed, else it will fall to the next condition
  if request.method == 'POST':
    form = acc_forms.PrivacyPage(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, f'Your account privacy is updated')
      return redirect(reverse('Profile', kwargs={'username':request.user}))
  else:
    form = acc_forms.PrivacyPage(instance=request.user)
    
  context = {
    'form':form,
  }
  return render(request, 'account/profile_privacy.html', context)




# This accountPasswordChange function allow user to change his account password
@login_required
def accountPasswordChange(request):
  form = acc_forms.PasswordChange(user=request.user, data=request.POST or None)
  if form.is_valid():
    form.save()
    update_session_auth_hash(request, form.user)
    messages.success(request, f'That sound great {request.user.first_name}, your password has been changed')
    return redirect(reverse('Profile', kwargs={'username':request.user}))
  return render(request, 'account/password_change.html', {'form':form})