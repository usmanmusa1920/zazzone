from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from account.models import FriendRequest
from blog.models import Post as Blog_Post
from zone.models import Zone
from board.models import Post as Board_Post
from django.contrib.auth.decorators import login_required
from .models import SearchHistory

from django.contrib.auth import get_user_model
User = get_user_model()




@login_required
def searchView(request):
  # This search_panel variable is the name attribute of search input field of this view template, and also it is a variable name included when paginating
  search_panel = request.GET.get('search_txt')
  
  # This is the current logged in user
  me = request.user
  
  # This filter all friend request
  friend_req_receiver_db = FriendRequest.objects.filter(Q(receiver=me))
  friend_req_send_db = FriendRequest.objects.filter(Q(sender=me))
  
  
  if search_panel == None or search_panel == '' or search_panel == ' ' or search_panel == '  ' or search_panel == '   ' or search_panel == '    ' or search_panel == '     ':
    pass
  
  # Here we search in our DB if the current user already searched that data so it will delete the previous one and then save the new one
  elif SearchHistory.objects.filter(user=me, data_to_search=search_panel):
    history_del = SearchHistory.objects.filter(user=me, data_to_search=search_panel)
    history_del.delete()
    
    history = SearchHistory(user=me, data_to_search=search_panel)
    history.save()
    
  # Here we save the search data if the user do not searched it already
  else:
    history = SearchHistory(user=me, data_to_search=search_panel)
    history.save()
  
  
  user_search_history = SearchHistory.objects.filter(user=me).order_by('-date')
      
  try:
    # This is a filter that filter user matching a giving query.
    users_filter = User.objects.filter(
      
      Q(first_name__exact=search_panel) | Q(first_name__iexact=search_panel) | Q(first_name__startswith=search_panel) | Q(first_name__istartswith=search_panel) | Q(first_name__contains=search_panel)| Q(first_name__icontains=search_panel)| Q(first_name__endswith=search_panel) | Q(first_name__iendswith=search_panel) |
      
      Q(last_name__exact=search_panel) | Q(last_name__iexact=search_panel) | Q(last_name__startswith=search_panel) | Q(last_name__istartswith=search_panel) | Q(last_name__contains=search_panel)| Q(last_name__icontains=search_panel)| Q(last_name__endswith=search_panel) | Q(last_name__iendswith=search_panel) |
      
      Q(username__exact=search_panel) | Q(username__iexact=search_panel) | Q(username__startswith=search_panel) | Q(username__istartswith=search_panel) | Q(username__contains=search_panel)| Q(username__icontains=search_panel)| Q(username__endswith=search_panel) | Q(username__iendswith=search_panel) | Q(phone_number=search_panel) | Q(email=search_panel)
      
      ).order_by('-date_joined')
  except:
    # This is a filter that filter user matching a giving query.
    users_filter = User.objects.filter(Q(first_name=search_panel) | Q(last_name=search_panel) | Q(username=search_panel) | Q(phone_number=search_panel) | Q(email=search_panel)).order_by('-date_joined')
  
  
  try:
    # This is a filter that filter blog post matching a giving query.
    blog_posts_db = Blog_Post.objects.filter(Q(title__istartswith=search_panel) | Q(title__contains=search_panel) | Q(text__istartswith=search_panel) | Q(code__istartswith=search_panel)).order_by('-last_modified')
  except:
    # This is a filter that filter blog post matching a giving query.
    blog_posts_db = Blog_Post.objects.filter(Q(title=search_panel) | Q(text=search_panel) | Q(code=search_panel)).order_by('-last_modified')
  
  
  try:
    # This is a filter that filter board post matching a giving query.
    board_posts_db = Board_Post.objects.filter(Q(title__istartswith=search_panel) | Q(text__istartswith=search_panel) | Q(code__istartswith=search_panel)).order_by('-last_modified')
  except:
    # This is a filter that filter board post matching a giving query.
    board_posts_db = Board_Post.objects.filter(Q(title=search_panel) | Q(text=search_panel) | Q(code=search_panel)).order_by('-last_modified')
  
  
  try:
    # This is a filter that filter zone matching a giving query.
    zones_db = Zone.objects.filter(Q(name__istartswith=search_panel) | Q(description__istartswith=search_panel)).order_by('-timestamp')
  except:
    # This is a filter that filter zone matching a giving query.
    zones_db = Zone.objects.filter(Q(name=search_panel) | Q(description=search_panel)).order_by('-timestamp')
  
  
  # This is user search history paginator
  paginator_history = Paginator(user_search_history, 3)
  page_0 = request.GET.get('page')
  searches = paginator_history.get_page(page_0)
  
  # This is users paginator
  paginator_users = Paginator(users_filter, 5)
  page_1 = request.GET.get('page')
  user_filter = paginator_users.get_page(page_1)
  
  # This is blog post paginator
  paginator_blog_posts = Paginator(blog_posts_db, 5)
  page_2 = request.GET.get('page')
  blog_posts = paginator_blog_posts.get_page(page_2)
  
  # This is board post paginator
  paginator_board_posts = Paginator(board_posts_db, 5)
  page_3 = request.GET.get('page')
  board_posts = paginator_board_posts.get_page(page_3)
  
  # This is zone paginator
  paginator_zones = Paginator(zones_db, 5)
  page_4 = request.GET.get('page')
  zone_filter = paginator_zones.get_page(page_4)
  
  # This is friend request for receivers paginator
  paginator_req_rec = Paginator(friend_req_receiver_db, 2)
  page_5 = request.GET.get('page')
  friend_req_receiver = paginator_req_rec.get_page(page_5)
  
  # This is friend request for senders paginator
  paginator_req_sen = Paginator(friend_req_send_db, 2)
  page_6 = request.GET.get('page')
  friend_req_send = paginator_req_sen.get_page(page_6)
  
  
  context = {
    'me':me,
    'search_panel':search_panel,
    'searches': searches,
    'friend_req_receiver': friend_req_receiver,
    'paginator_req_rec': paginator_req_rec,
    'friend_req_send': friend_req_send,
    'paginator_req_sen': paginator_req_sen,
    'user_filter':user_filter,
    'paginator_users':paginator_users,
    'blog_posts_db': blog_posts,
    'paginator_blog_posts': paginator_blog_posts,
    'board_posts_db': board_posts,
    'paginator_board_posts': paginator_board_posts,
    'zones_db': zone_filter,
    'paginator_zones': paginator_zones,
  }
  return render(request, 'search/search_result.html', context)




@login_required
def deleteSearch(request, search_id):
  
  find_match_id = SearchHistory.objects.get(id=search_id)
  if find_match_id.user == request.user:
    find_match_id.delete()
    return redirect(reverse('search'))
  return False