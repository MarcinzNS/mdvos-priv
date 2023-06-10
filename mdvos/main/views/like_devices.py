from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from main.models.models import Devices, Like



@login_required
def add_like(request, device_id):
    user=request.user
    device = get_object_or_404(Devices, pk=device_id)

    # Sprawdź, czy użytkownik ma już niepolubienie dla tego urządzenia
    existing_dislike = Like.objects.filter(user_id=user, devices_id=device, dislike=True).first()
    if existing_dislike:
        existing_dislike.delete()  # Usuń dislike

    like = Like(user_id=user, devices_id=device, like=True, dislike=False)
    like.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def add_dislike(request, device_id):
    user=request.user
    device = get_object_or_404(Devices, pk=device_id)

    # Sprawdź, czy użytkownik ma już like dla tego urządzenia
    existing_like = Like.objects.filter(user_id=user, devices_id=device, like=True).first()
    if existing_like:
        existing_like.delete()  # Usuń like

    dislike = Like(user_id=user, devices_id=device, like=False, dislike=True)
    dislike.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def remove_like(request, device_id):
    device = get_object_or_404(Devices, pk=device_id)
    user=request.user
    like = Like.objects.filter(user_id=user, devices_id=device, like=True).first()
    if like:
        like.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def remove_dislike(request, device_id):
    device = get_object_or_404(Devices, pk=device_id)
    user=request.user
    dislike = Like.objects.filter(user_id=user, devices_id=device, dislike=True).first()
    if dislike:
        dislike.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])