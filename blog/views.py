import os
from django.shortcuts import reverse, redirect
from .models import Post, Comment
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from board.models import Post as board_post_model, Board
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from chat.models import Message
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Home(LoginRequiredMixin, ListView):
    model = board_post_model
    paginate_by = 5
    ordering = ['-last_modified']
    context_object_name = 'posts'
    template_name = 'blog/home.html'

    def get_context_data(self):
        board_post = board_post_model.objects.all().order_by('-last_modified')
        blog_post = Post.objects.all().order_by('-last_modified')
        unread_msg = Message.objects.filter(to_receiver=self.request.user.id, is_view=False)

        context = {
            'board_post': board_post,
            'blog_post': blog_post,
            'unread_msg': unread_msg
        }
        if unread_msg.count() >= 20:
            messages.success(
                self.request, f'{self.request.user.first_name} you have {unread_msg.count()} unread messages')
        return super().get_context_data(**context)
    
    def get_queryset(self):
        return board_post_model.objects.all().order_by('-pub_date')
    

class BlogHome(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 5
    ordering = ['-last_modified']
    context_object_name = 'posts'
    template_name = 'blog/blog_home.html'

    def get_context_data(self):
        board = Post.objects.all().order_by('-last_modified')
        # board = Post.objects.filter(publisher=user.objects.get(username='Shehu'))

        unread_msg = Message.objects.filter(
            to_receiver=self.request.user.id, is_view=False)
        # for friend in self.request.user.friends.all():
        #   board = Post.objects.filter(publisher=friend).order_by('-last_modified')
        #   # print(board, '\n', end='\n')
        #   # print(dir(board))
        #   for i in board:
        #     if i.text:
        #       print(i.id, i.text, i.publisher, '((' + str(i.last_modified) + '))')
        #     else:
        #       print(i.id, 'NOOO', i.publisher, '((' + str(i.last_modified) + '))')
        #     print()
        # for b in Post.objects.all().order_by('-last_modified'):
        
        #   if b.publisher in self.request.user.friends.all():
        #     board = b
        #     print(board)

        context = {
            'board': board,
            'unread_msg': unread_msg
        }
        return super().get_context_data(**context)
    
    def get_queryset(self):
        return Post.objects.all().order_by('-last_modified')
    

class BlogDetail(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
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
            Comment.objects.create(commentator=name, body=body, post=post)
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
def blogPostLike(request, post_id):
    post_to_like = Post.objects.get(id=post_id)
    if request.user not in post_to_like.likers.all():
        post_to_like.likers.add(request.user)
        return redirect(reverse('Blog_Detail', kwargs={'pk': post_id}))
    else:
        post_to_like.likers.remove(request.user)
        return redirect(reverse('Blog_Detail', kwargs={'pk': post_id}))
    

class BlogCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/blog_create.html'
    fields = ['title', 'image', 'text', 'code']

    def form_valid(self, form):
        title = form.cleaned_data['title']
        image = form.cleaned_data['image']
        text = form.cleaned_data['text']
        code = form.cleaned_data['code']
        if title == None and text == '' and code == '' and image == None:
            return self.render_to_response({'form': form})
        form.instance.publisher = self.request.user
        if not self.request.user in self.request.user.friends.all():
            self.request.user.friends.add(self.request.user)

        my_board = Board.objects.get(owner=self.request.user.id)
        if self.request.user not in my_board.followers.all():
            my_board.followers.add(self.request.user.id)
        return super().form_valid(form)
    

class BlogEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/blog_edit.html'
    fields = ['title', 'image', 'text', 'code']

    def form_valid(self, form):
        title = form.cleaned_data['title']
        text = form.cleaned_data['text']
        code = form.cleaned_data['code']
        image = form.cleaned_data['image']

        if title == None and text == '' and code == '' and image == None:
            messages.success(
                self.request, f'At this moment one of these field is required')
            return self.render_to_response({'form': form})
        form.instance.publisher = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.publisher:
            return True
        return False
    

class BlogEditImage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/blog_img_update.html'
    fields = ['title', 'image', 'text', 'code']

    def form_valid(self, form):
        title = form.cleaned_data['title']
        text = form.cleaned_data['text']
        code = form.cleaned_data['code']
        image = form.cleaned_data['image']

        if title == None and text == '' and code == '' and image == None:
            return self.render_to_response({'form': form})
        post = self.get_object()
        if self.request.user == post.publisher:
            if post.image:
                r = post.image.path
                if os.path.exists(r):
                    os.remove(r)
        form.instance.publisher = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.publisher:
            return True
        return False
    

class BlogDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/blog_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.publisher:
            return True
        return False
    
    def form_valid(self, form):
        post = self.get_object()
        if self.request.user == post.publisher:
            if post.image:
                r = post.image.path
                os.remove(r)
        return super().form_valid(form)
