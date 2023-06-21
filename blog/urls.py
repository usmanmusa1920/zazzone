from django.urls import path
from . import views as blog_views


urlpatterns = [
    path(
        '', blog_views.Home.as_view(), name='Home'),
    path(
        'post/', blog_views.BlogHome.as_view(), name='Blog_Home'),
    path(
        'post/<int:pk>/', blog_views.BlogDetail.as_view(), name='Blog_Detail'),
    path(
        'post_like/<int:post_id>/', blog_views.blogPostLike, name='blog_like'),
    path(
        'new_post/', blog_views.BlogCreate.as_view(), name='Blog_Create'),
    path(
        'post_update/<int:pk>/', blog_views.BlogEdit.as_view(), name='Blog_Edit'),
    path(
        'post_image_update/<int:pk>/', blog_views.BlogEditImage.as_view(), name='Blog_Edit_Image'),
    path(
        'delete_post/<int:pk>/', blog_views.BlogDelete.as_view(), name='Blog_Delete'),
]
