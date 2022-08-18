from django.urls import path
from . import views as zone_view




urlpatterns = [
  path('<str:username>/zone_create/', zone_view.ZoneCreate.as_view(), name='Zone_Create'),
  path('<str:username>/zone/', zone_view.zoneHome, name='zone_home'),
  path('<str:user_pk>/<int:id>/new_member/', zone_view.memberAdd, name='add_member'),
  path('<int:zone_id>/join_zone/', zone_view.joinZone, name='join_zone'),
  path('<int:zone_id>/edit/image/', zone_view.updateZoneImage, name='edit_zone_image'),
  path('<int:zone_id>/edit/info/', zone_view.updateZoneInfo, name='edit_zone_info'),
  path('<str:user_pk>/<int:id>/remove_member/', zone_view.memberRemove, name='remove_member'),
  path('<int:zone_id>/leave_zone/', zone_view.leaveZone, name='leave_zone'),
  path('<int:zone_id>/zone_message/', zone_view.sendMessage, name='zone_message'),
  path('<int:zone_id>/<str:username>/zone_detail/', zone_view.zoneDetail, name='zone_detail'),
  path('<str:username>/<int:zone_id>/delete_zone/', zone_view.deleteZone, name='delete_zone'),
]