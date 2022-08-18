from django.urls import path
from . import views as board_views




app_name = 'board'

urlpatterns = [
  path('board/<str:username>/', board_views.BoardHome.as_view(), name='Board_Home'),
  path('user/board/<int:board_id>/', board_views.user_board, name='board'),
  path('board/<int:pk>/<str:username>/', board_views.BoardDetail.as_view(), name='Board_Detail'),
  path('board/like/<int:post_id>/<str:username>/', board_views.boardPostLike, name='board_post_like'),
  path('new_board/<str:username>/', board_views.BoardCreate.as_view(), name='Board_Create'),
  path('board_update/<int:pk>/<str:username>/', board_views.BoardEditPostText.as_view(), name='Board_Edit'),
  path('board_image_update/<int:pk>/<str:username>/', board_views.BoardEditPostImage.as_view(), name='Board_Edit_Image'),
  path('delete_board/<int:pk>/<str:username>/', board_views.BoardDelete.as_view(), name='Board_Delete'),
  path('follow_board/<int:user_id>/', board_views.followBoard, name='follow_board'),
  path('unfollow_board/<int:user_id>/', board_views.unfollowBoard, name='unfollow_board'),
]