from .models import Post, Comment, Board
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, BoardImageUpdate, BoardInfoUpdate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator

from django.conf import settings
User = settings.AUTH_USER_MODEL

from django.contrib.auth import get_user_model
User_get = get_user_model()

import os




class BoardHome(LoginRequiredMixin, ListView):
  model = Post
  paginate_by = 5
  ordering = ['-last_modified']
  context_object_name = 'posts'
  template_name = 'board/board_home.html'
  
  def get_context_data(self):
    # board = Post.objects.all().order_by('-last_modified')
      
    context = {
      # 'board': board
    }
    return super().get_context_data(**context)
  
  def get_queryset(self):
    return Post.objects.all().order_by('-pub_date')
  
  
  
  
@login_required
def user_board(request, board_id):
  view_user_board = Board.objects.get(id=board_id)
  post = Post.objects.filter(publisher=view_user_board.owner.board_owner).order_by('-pub_date')
  
  paginator = Paginator(post, 5)
  page = request.GET.get('page')
  user_board_posts = paginator.get_page(page)
  
  followers = view_user_board.followers.all()
  
  context = {
    'view_user_board': view_user_board,
    'followers': followers,
    'user_board_posts': user_board_posts,
    'user_board_posts_count': post,
  }
  return render(request, 'board/user_board.html', context)
  
  
  
  
class BoardDetail(LoginRequiredMixin, DetailView):
  model = Post
  context_object_name = 'post'
  template_name = 'board/board_detail.html'
  
  def get_context_data(self,**kwargs):
    context = super().get_context_data(**kwargs)
    pk = self.kwargs['pk']
    form = CommentForm()
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.all().order_by('-com_date')
    context['post'] = post
    context['form'] = form
    
    paginator = Paginator(comments, 5)
    page_1 = self.request.GET.get('page')
    comment = paginator.get_page(page_1)
    
    context['comments_1'] = comment
    context['comments_2'] = comments
    
    return context
  
  def post(self, request, *args, **kwargs):
    form = CommentForm(request.POST)
    self.object = self.get_object()
    context = super().get_context_data(**kwargs)
    post = Post.objects.filter(id=self.kwargs['pk'])[0]
    comments = post.comment_set.all().order_by('-com_date')
    context['post'] = post
    context['form'] = form
    
    if form.is_valid():
      name = self.request.user
      body = form.cleaned_data['body']
      Comment.objects.create(commentator = name, body = body, post = post)
      form = CommentForm()
      context['form'] = form
    
      paginator = Paginator(comments, 5)
      page_2 = self.request.GET.get('page')
      comment = paginator.get_page(page_2)
      
      context['comments_1'] = comment
      context['comments_2'] = comments
      
      return self.render_to_response(context)
    
    return self.render_to_response(context=context)
  
  
  
  
@login_required
def boardPostLike(request, post_id, username):
  post_to_like = Post.objects.get(id=post_id)
  if request.user not in post_to_like.likers.all():
    post_to_like.likers.add(request.user)
    return redirect(reverse('board:Board_Detail', kwargs={'pk':post_id, 'username': request.user}))
  else:
    post_to_like.likers.remove(request.user)
    return redirect(reverse('board:Board_Detail', kwargs={'pk':post_id, 'username': request.user}))
  
  
  
  
class BoardCreate(LoginRequiredMixin, CreateView):
  model = Post
  template_name = 'board/board_create.html'
  fields = ['title', 'image', 'text', 'code']
  
  def form_valid(self, form):
    title = form.cleaned_data['title']
    image = form.cleaned_data['image']
    text = form.cleaned_data['text']
    code = form.cleaned_data['code']
  
    if title == None and text == '' and code == '' and image == None:
      return self.render_to_response({'form':form})
    form.instance.publisher = self.request.user.board_owner
    if not self.request.user in self.request.user.friends.all():
      self.request.user.friends.add(self.request.user)
    
    my_board = Board.objects.get(owner=self.request.user.id)
    if self.request.user not in my_board.followers.all():
      my_board.followers.add(self.request.user.id)
      
    return super().form_valid(form)
  
  
  
  
class BoardEditPostText(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  context_object_name = 'posts'
  template_name = 'board/board_post_edit.html'
  fields = ['title', 'image', 'text', 'code']
  
  def form_valid(self, form):
    title = form.cleaned_data['title']
    text = form.cleaned_data['text']
    code = form.cleaned_data['code']
    image = form.cleaned_data['image']
    
    if title == None and text == '' and code == '' and image == None:
      messages.success(self.request, f'At this moment one of these field is required')
      return self.render_to_response({'form':form})
    form.instance.publisher = self.request.user.board_owner
    return super().form_valid(form)
  
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.publisher.owner:
      return True
    return False
  
  
  
  
class BoardEditPostImage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  context_object_name = 'posts'
  template_name = 'board/board_img_update.html'
  fields = ['title', 'image', 'text', 'code']
  
  def form_valid(self, form):
    title = form.cleaned_data['title']
    text = form.cleaned_data['text']
    code = form.cleaned_data['code']
    image = form.cleaned_data['image']
    
    if title == None and text == '' and code == '' and image == None:
      return self.render_to_response({'form':form})
    post = self.get_object()
    if self.request.user == post.publisher.owner:
      if post.image:
        r = post.image.path
        if os.path.exists(r):
          os.remove(r)
    form.instance.publisher = self.request.user.board_owner
    return super().form_valid(form)
  
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.publisher.owner:
      return True
    return False
  
  
  
  
class BoardDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  success_url = '/'
  template_name = 'board/board_delete.html'
  
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.publisher.owner:
      return True
    return False
  
  def form_valid(self, form):
    post = self.get_object()
    if self.request.user == post.publisher.owner:
      if post.image:
        r = post.image.path
        if os.path.exists(r):
          os.remove(r)
    return super().form_valid(form)
  
  
  
  
@login_required
def followBoard(request, user_id):
  board = Board.objects.get(owner=user_id)
  if request.user not in board.followers.all():
    board.followers.add(request.user.id)
    messages.success(request, f'You are now a follower in this board ({board.owner.first_name} {board.owner.last_name})')
    return redirect(reverse('board:board', kwargs={'board_id':board.id}))
  else:
    messages.success(request, f'You are already already a follower in this board ({board.owner.first_name} {board.owner.last_name})')
    return redirect(reverse('board:board', kwargs={'board_id':board.id}))
  
  
  
  
@login_required
def unfollowBoard(request, user_id):
  board = Board.objects.get(owner=user_id)
  if request.user not in board.followers.all():
    messages.success(request, f'You are not a follower in this board ({board.owner.first_name} {board.owner.first_name})')
    return redirect(reverse('board:board', kwargs={'board_id':board.id}))
  else:
    board.followers.remove(request.user.id)
    messages.success(request, f'You removed your self from ' + str(board.owner.first_name) + ' board')
    return redirect(reverse('board:board', kwargs={'board_id':board.id}))
  
  
  
  
# This boardInfoUpdate function it will update the current login user board information, but with an exception of media files such as board image
@login_required
def boardInfoUpdate(request):
  
  # Here we check if the request method is POST then it will proceed, else it will return the user to the board update page together with his current board in
  if request.method == 'POST':
    form = BoardInfoUpdate(request.POST, instance=request.user.board_owner)
    if form.is_valid():
      form.save()
      messages.success(request, f'Your board info has been updated!')
      return redirect(reverse('board:board', kwargs={'board_id':request.user.id}))
  else:
    form = BoardInfoUpdate(instance=request.user.board_owner)
    
  context = {
    'form':form,
  }
  return render(request, 'board/board_info_update.html', context)




# This boardImageUpdate function it will update the current login user board image only
@login_required
def boardImageUpdate(request):
  
  # Here we check if the request method is POST then it will proceed, else it will return the user to the board image update page together with his current board information with an exception of media files like image
  if request.method == 'POST':
    form = BoardImageUpdate(request.POST, request.FILES, instance=request.user.board_owner)
    r = request.user.board_owner.image.path
    print(r)
    if form.is_valid():
      if r != '/home/usman/Desktop/acode/sakyum/sakyum/media/board_default_img.jpg':
        if os.path.exists(r):
          os.remove(r)
      form.save()
      messages.success(request, f'Your board image has been updated!')
      return redirect(reverse('board:board', kwargs={'board_id':request.user.id}))
  else:
    form = BoardImageUpdate(instance=request.user.board_owner)
    
  context = {
    'form': form,
  }
  return render(request, 'board/board_image_update.html', context)