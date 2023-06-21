import os
from pathlib import Path
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Zone, Message
from .forms import ZoneCreatForm, ZoneUpdateImage, ZoneUpdateInfo, MessageForm
from django.contrib.auth import get_user_model


User = get_user_model()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def zoneHome(request, username):
    zone_i_am_in = Zone.objects.filter(members=request.user).order_by('-timestamp')
    zone_i_am_not_in = Zone.objects.exclude(members=request.user).order_by('-timestamp')

    # pagination of zones that i am in
    paginator = Paginator(zone_i_am_in, 5)
    page_1 = request.GET.get('page')
    zones = paginator.get_page(page_1)

    # pagination of zones that i am not in
    paginator = Paginator(zone_i_am_not_in, 5)
    page_2 = request.GET.get('page')
    zones_not_in = paginator.get_page(page_2)

    context = {
        'zones': zones,
        'zones_not_in': zones_not_in
    }
    return render(request, 'zone/zone.html', context)


class ZoneCreate(FormView):
    form_class = ZoneCreatForm
    template_name = 'zone/zone_create.html'
    context_object_name = 'zone'

    def get_success_url(self):
        return reverse("zone_home", kwargs={"username": self.request.user})
    
    def form_valid(self, form):
        name = form.cleaned_data['name']
        zone_type = form.cleaned_data['zone_type']
        custom_type = form.cleaned_data['custom_zone_type']
        form.instance.creator = self.request.user

        instance = form.save(commit=False)
        if zone_type == 'business' or zone_type == 'public' or zone_type == 'school' or zone_type == 'family':
            pass
            instance.custom_zone_type = zone_type
        else:
            instance.custom_zone_type = custom_type
        instance.save()
        instance.members.add(self.request.user.id)

        messages.success(
            self.request, f'Your just create a new zone ({name} zone)')
        return super().form_valid(form)
    

def updateZoneImage(request, zone_id):
    zone = Zone.objects.get(id=zone_id)
    if request.user == zone.creator:
        if request.method == 'POST':
            form = ZoneUpdateImage(request.POST, request.FILES, instance=zone)
            r = zone.image.path
            if form.is_valid():
                default_img_path = os.path.join(BASE_DIR, 'media/zone_default_img.jpg')
                if r != default_img_path:
                    if os.path.exists(r):
                        os.remove(r)
                form.save()
                messages.success(request, f'Your zone image has been updated!')
                return redirect(reverse('zone_message', kwargs={'zone_id': zone_id}))
        else:
            form = ZoneUpdateImage(instance=zone)
        context = {
            'zone': zone,
            'form': form,
        }
        return render(request, 'zone/zone_img_update.html', context)
    else:
        return False
    

def updateZoneInfo(request, zone_id):
    zone = Zone.objects.get(id=zone_id)
    if request.user == zone.creator:
        if request.method == 'POST':
            form = ZoneUpdateInfo(request.POST, instance=zone)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your zone info has been updated!')
                return redirect(reverse('zone_message', kwargs={'zone_id': zone_id}))
        else:
            form = ZoneUpdateInfo(instance=zone)
        context = {
            'zone': zone,
            'form': form,
        }
        return render(request, 'zone/zone_info_update.html', context)
    else:
        return False
    

def deleteZone(request, username, zone_id):
    zone = Zone.objects.get(id=zone_id)
    r = zone.image.path
    if request.user == zone.creator:
        default_img_path = os.path.join(BASE_DIR, 'media/zone_default_img.jpg')
        if r != default_img_path:
            if os.path.exists(r):
                os.remove(r)
        zone.delete()
        messages.success(
            request, f'You just deleted your zone (' + str(zone.name) + ')')
        return redirect(reverse('zone_home', kwargs={'username': username}))
    else:
        return False
    

def sendMessage(request, zone_id, username=False):
    msg = Message.objects.filter(zone_id=zone_id).order_by('-timestamp')
    zone = Zone.objects.get(id=zone_id)
    me = request.user

    paginator = Paginator(msg, 6)
    page = request.GET.get('page')
    message = paginator.get_page(page)
    
    search_panel = request.GET.get('search_txt')
    users_filter = User.objects.filter(
        Q(first_name=search_panel) | Q(last_name=search_panel) | Q(username=search_panel) | Q(phone_number=search_panel) | Q(email=search_panel)).order_by('-date_joined')
    
    if me in zone.members.all():
        if request.method == 'POST':
            form = MessageForm(request.POST, request.FILES)
            if form.is_valid():
                if form.cleaned_data.get('image') == None and form.cleaned_data.get('message') == '':
                    messages.success(request, f'You can\'t send blank space (empty)')
                    return redirect(reverse('zone_message', kwargs={'zone_id': zone_id}))
                instance = form.save(commit=False)
                instance.zone_sender = request.user
                instance.zone = zone
                instance.save()
                return redirect(reverse('zone_message', kwargs={'zone_id': zone_id}))
        context = {
            'message': message,
            'zone': zone,
            'users_filter': users_filter,
        }
        return render(request, 'zone/zone_message.html', context)
    else:
        return redirect(reverse('zone_detail', kwargs={'zone_id': zone_id, 'username': me}))
    

@login_required
def zoneDetail(request, zone_id, username=False):
    zone = Zone.objects.get(id=zone_id)

    # paginator = Paginator(msg, 6)
    # page = request.GET.get('page')
    # message = paginator.get_page(page)

    context = {
        'zone': zone,
    }
    if request.user in zone.members.all():
        return render(request, 'zone/zone_detail.html', context)
    else:
        messages.success(
            request, f'You are not a member, try to join the zone in other to send message in the zone')
        return render(request, 'zone/zone_detail.html', context)
    

@login_required
def memberAdd(request, user_pk, id):
    add_member = User.objects.get(id=user_pk)
    zone = Zone.objects.get(id=id)
    if zone.creator == request.user:
        if add_member in zone.members.all():
            messages.success(
                request, f'{add_member.first_name} {add_member.last_name} was already a member in this zone')
            return redirect(reverse('zone_detail', kwargs={'zone_id': id, 'username': request.user}))
        else:
            zone.members.add(add_member.id)
            messages.success(
                request, f'You just added a new member in this zone ({add_member.first_name} {add_member.last_name})')
            return redirect(reverse('zone_detail', kwargs={'zone_id': id, 'username': request.user}))
    else:
        return False
    

@login_required
def memberRemove(request, user_pk, id):
    remove_member = User.objects.get(id=user_pk)
    zone = Zone.objects.get(id=id)
    if zone.creator == request.user:
        if remove_member in zone.members.all():
            if remove_member != zone.creator:
                zone.members.remove(remove_member.id)
                for member_msg in Message.objects.filter(zone=zone, zone_sender=remove_member):
                    if member_msg.image:
                        r = member_msg.image.path
                        if os.path.exists(r):
                            os.remove(r)
                    member_msg.delete()
                messages.success(
                    request, f'You just remove a member in this zone ({remove_member.first_name} {remove_member.last_name})')
                return redirect(reverse('zone_detail', kwargs={'zone_id': id, 'username': request.user}))
            else:
                messages.success(
                    request, f'Zone admin can\'t remove him self from his zone ({remove_member.first_name} {remove_member.last_name})')
                return redirect(reverse('zone_detail', kwargs={'zone_id': id, 'username': request.user}))
        else:
            messages.success(
                request, f'{remove_member.first_name} {remove_member.last_name} is not a member in this zone ({zone.name})')
            return redirect(reverse('zone_detail', kwargs={'zone_id': id, 'username': request.user}))
    else:
        return False
    

@login_required
def leaveZone(request, zone_id):
    zone = Zone.objects.get(id=zone_id)
    if request.user in zone.members.all():
        zone.members.remove(request.user)
        for member_msg in Message.objects.filter(zone=zone, zone_sender=request.user):
            if member_msg.image:
                r = member_msg.image.path
                if os.path.exists(r):
                    os.remove(r)
            member_msg.delete()
        messages.success(
            request, f'You removed your self from ' + str(zone.name) + ' zone')
        return redirect(reverse('zone_home', kwargs={'username': request.user}))
    else:
        return False
    
    
@login_required
def joinZone(request, zone_id):
    zone = Zone.objects.get(id=zone_id)
    if request.user not in zone.members.all():
        zone.members.add(request.user.id)
        messages.success(
            request, f'You are now a member in this zone ({zone.name})')
        return redirect(reverse('zone_message', kwargs={'zone_id': zone_id}))
    else:
        messages.success(
            request, f'You are already already a member in this zone ({zone.name})')
        return redirect(reverse('zone_message', kwargs={'zone_id': zone_id}))
