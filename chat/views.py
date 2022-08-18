from django.shortcuts import render, redirect, reverse
from .models import Message
from . import forms as msg_forms
from django.contrib import messages
from account.models import FriendRequest
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()




@login_required
def chat(request, username):
  # This is the current user instance
  me = request.user
  
  # Here we filter friend request sent tothe current user
  friend_req = FriendRequest.objects.filter(Q(receiver=request.user))
  
  # At this one we filter a query that will retrieve messages that the receiver of it is the current user, the is_msg_added=True. and the is_new_message=False, OR the receiver of it (messages) is the current user, the is_msg_added=False. and the is_new_message=False, OR the sender of it (messages) is the current user, the is_msg_added=False. and the is_new_message=False, OR the sender of it (messages) is the current user, the is_msg_added=True. and the is_new_message=False,
  msgs_filter = Message.objects.filter(to_receiver=request.user.id, is_msg_added=False, is_new_message=False).order_by('-timestamp') | Message.objects.filter(to_receiver=request.user.id, is_msg_added=True, is_msg_replied=False).order_by('-timestamp') | Message.objects.filter(from_sender=request.user.id, is_msg_added=False, is_new_message=False).order_by('-timestamp') | Message.objects.filter(from_sender=request.user.id, is_msg_added=True, is_msg_replied=False).order_by('-timestamp')
  
  paginator = Paginator(msgs_filter, 6)
  page = request.GET.get('page')
  msgs = paginator.get_page(page)
  
  # Here we filter the messages that was sent to the current user, but yet he/she didn't view (read) it
  unread_msg = Message.objects.filter(to_receiver=request.user.id, is_view=False)
  
  context = {
    'me': me,
    'friend_req': friend_req,
    'unread_msg': unread_msg,
    'msgs': msgs,
    'paginator_count': paginator
  }
  return render(request, 'chat/chat.html', context)



@login_required
def sendMessage(request, user_id):
  # This one we filter all users of this platform
  users = User.objects.all()
  
  # This one we filter a user by his id (user_id), which will allow us to goto his/her message page
  my_friend = User.objects.get(id=user_id)
  # Here we filter the messages that was sent to the current user, but yet he/she didn't view (read) it
  unread_msg = Message.objects.filter(to_receiver=request.user.id, is_view=False)
  
  
  # This try block we check if there is any message where the receiver of it is the current user (the last message of the query set).
  try:
    is_seen = Message.objects.filter(to_receiver=request.user.id, from_sender=my_friend).last()
    if is_seen.to_receiver == request.user:
      # At this one we filter messages where the receiver is the current user and the is_view of the message is equal to False
      is_msg_view = Message.objects.filter(to_receiver=request.user.id, from_sender=my_friend, is_view=False)
      
      # Here we do a for loop in which it will make all messages where the receiver is the current user and the is_view = False, then it will convert the is_view from False to True
      for msg in is_msg_view:
        msg.is_view = True
        msg.save()
  except:
    pass
  
  
  # In this we filter messages where the receiver is the current user and the sender is the user we are in his message page OR vice versal
  msg = Message.objects.filter(Q(from_sender=request.user, to_receiver=my_friend) | Q(from_sender=my_friend, to_receiver=request.user)).all().order_by('-timestamp')
  
  # This is the pagination of the above query set (msg)
  paginator = Paginator(msg, 6)
  page = request.GET.get('page')
  message = paginator.get_page(page)
  
  
  # It is the context of the message paginator
  context = {'message':message}
  
  # Here we check if the user we view his message page is in the current user friend list, else it will fall to the else condition
  if my_friend in request.user.friends.all():
    # Current user
    user = request.user
    
    # Checking for the request method
    if request.method == 'POST':
      m_form = msg_forms.MessageForm(request.POST, request.FILES)
      if m_form.is_valid():
        # Checking if the cleaned_data of image == None and cleaned_dat of message == empty
        if m_form.cleaned_data.get('image') == None and m_form.cleaned_data.get('message') == '':
          messages.warning(request, f'You can\'t send space (empty)')
          return redirect(reverse('send_message', kwargs={'user_id':user_id}))
          
        # Here it will try by filtering Messages where the sender is the current loged in user and the receiver is the friend (the one you are in his messages page)
        try:
          get_msgs_1 = Message.objects.filter(from_sender=request.user.id, to_receiver=my_friend).last()
          if get_msgs_1.from_sender == request.user:
            
            # This is if wheather the previous messages are not marked as is_msg_added, then the below condition will make them (mark as is_msg_added)
            is_new_msg = Message.objects.filter(from_sender=request.user.id, to_receiver=my_friend, is_msg_added=False, is_new_message=False) | Message.objects.filter(from_sender=request.user.id, to_receiver=my_friend, is_msg_added=True, is_new_message=False)
            
            for msg in is_new_msg:
              msg.is_new_message = True
              msg.save()
        except:
          pass
        
        # Here it will try by filtering Messages where the receiver is the current loged in user and the sender is the friend (the one you are in his messages page)
        try:
          get_msgs_2 = Message.objects.filter(to_receiver=request.user.id, from_sender=my_friend).last()
          if get_msgs_2.to_receiver == request.user:
            # This is if the message is replied
            is_replied_msg = Message.objects.filter(to_receiver=request.user.id, from_sender=my_friend, is_msg_replied=False)
            
            for msg in is_replied_msg:
              msg.is_msg_replied = True
              msg.is_msg_added = True
              msg.save()
        except:
          pass
          
        instance = m_form.save(commit=False)
        instance.to_receiver = my_friend
        instance.from_sender = user
        instance.save()
          
        return redirect(reverse('send_message', kwargs={'user_id':user_id}))
    context = {
      'message': message,
      'friend': my_friend,
      'unread_msg': unread_msg,
      'user': user,
      'users': users
    }
    return render(request, 'chat/chat_message.html', context)
  
  else:
    sender = request.user
    receiver = User.objects.get(id=user_id)
    for friend in FriendRequest.objects.all():
      if friend.sender == receiver and friend.receiver == sender:
        if receiver.gender == 'female':
          messages.success(request, f'You must accept {receiver.first_name} friend request in other to chat with her')
          return redirect(reverse('search', kwargs={'username':sender}))
        else:
          messages.success(request, f'You must accept {receiver.first_name} friend request in other to chat with him')
          return redirect(reverse('search'))
    
    friend_request, created = FriendRequest.objects.get_or_create(sender=sender,receiver=receiver)
    if created:
      if receiver.gender == 'female':
        messages.success(request, f'{receiver.first_name} is not in your friend list, but friend request was sent to her')
      else:
        messages.success(request, f'{receiver.first_name} is not in your friend list,  but friend request was sent to him')
      return redirect(reverse('profile_user', kwargs={'username':receiver}))
    else:
      if receiver.gender == 'female':
        messages.success(request, f'{receiver.first_name} is not in your friend list, but friend request was already sent to her')
      else:
        messages.success(request, f'{receiver.first_name} is not in your friend list, but friend request was already sent to him')
      return redirect(reverse('profile_user', kwargs={'username':receiver}))
    return False