"""zazzone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin

from search import views as search_view
from account import views as acc_view
# from blog import views as blog_views
from board import views as board_views
from chat import views as chat_view
from iratio import views as iratio_view
# from zone import views as zone_view


class LoginCustom(LoginView):
    def get_context_data(self, **kwargs):
        the_year = datetime.today().year
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'the_year': the_year,
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context
    

class LogoutCustom(LoginRequiredMixin, LogoutView):
    the_year = datetime.today().year

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            'the_year': self.the_year,
            'site': current_site,
            'site_name': current_site.name,
            # 'title': _('Logged out'),
            **(self.extra_context or {})
        })
        return context
    

urlpatterns = [
    # accout
    path(
        'signup/', acc_view.signupView, name='signup'),
    path(
        'password_change/', acc_view.accountPasswordChange, name='password_change'),

    # auth
    path(
        'admin/', admin.site.urls),
    path(
        'login/', LoginCustom.as_view(template_name='account/login.html'), name='login'),
    path(
        'logout/', LogoutCustom.as_view(template_name='account/logout.html'), name='logout'),

    # board (not all)
    path(
        'board/img/update/', board_views.boardImageUpdate, name='board_img_update'),
    path(
        'board/info/update/', board_views.boardInfoUpdate, name='board_info_update'),

    # search
    path(
        'search/', search_view.searchView, name='search'),
    path(
        '<int:search_id>/', search_view.deleteSearch, name='delete_search'),

    # chat
    path(
        '<str:username>/chat/', chat_view.chat, name='chat'),
    path(
        '<int:user_id>/message/', chat_view.sendMessage, name='send_message'),

    # iratio
    path(
        '<str:username>/<int:user_id>/iratio/', iratio_view.iratio, name='iratio'),
    path(
        '<str:username>/new/iratio/', iratio_view.iratioNew, name='iratio_new'),

    # account
    path(
        'about/', acc_view.about, name='about'),
    path(
        'delete_message_us/<int:message_id>/', acc_view.deleteMessageUs, name='delete_message_us'),
    path(
        'mark_message_us/<int:message_id>/', acc_view.markMessageUs, name='mark_message_us'),
    path(
        'contact/#contact_page/', acc_view.about, name='contact'),
    path(
        'privacy/#privacy_page/', acc_view.about, name='privacy'),

    # profile
    path(
        '<str:username>/', acc_view.UserProfile.as_view(), name='Profile'),
    path(
        '<str:username>/profile/', acc_view.viewUserProfile, name='profile_user'),
    path(
        '<str:username>/gallery/', acc_view.UserGallery.as_view(), name='Gallery'),
    path(
        'gallery/<str:username>/', acc_view.viewUserGallery, name='gallery_user'),

    # update
    path(
        'profile/update/', acc_view.profileUpdate, name='profile_update'),
    path(
        'privacy/update/', acc_view.privacyMe, name='privacy_page'),
    path(
        'image/update/', acc_view.imageUpdate, name='image_update'),
    path(
        'banner/update/', acc_view.bannerUpdate, name='banner_update'),

    # friend
    path(
        '<int:req_pk>/friend_request_send/', acc_view.sendFriendRequest, name='friend_request'),
    path(
        '<int:req_pk>/friend_request/', acc_view.acceptFriendRequest, name='friend_request_accept'),
    path(
        '<int:user_pk>/friend_remove/', acc_view.removeFriend, name='friend_remove'),
    path(
        '<int:req_pk>/decline_request/', acc_view.declineRequest, name='decline_request'),

    # modules urls
    path('', include('zone.urls')),
    path('', include('blog.urls')),
    path('', include('board.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
