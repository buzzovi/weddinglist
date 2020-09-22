import re
from datetime import date, timedelta, datetime

import requests
from django.template import loader
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.utils.html import strip_tags
from rest_framework import permissions, viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from weddinglist.models import Pokemon
from weddinglist.serializers import (UserSerializer, GroupSerializer,
                                     GiftSerializer,
                                     GiftListSerializer,)
from weddinglist.models import Gift, GiftList, User, GiftListItem


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class GiftListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows GiftList to be viewed.
    """

    queryset = GiftList.objects.all()
    serializer_class = GiftListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', '=id']


class GiftViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows GiftList to be viewed.
    """
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', '=id']


@api_view(['POST'])
def PurchaseGift(request, gift_list_item_id):
    """
    Purchase a gift from the list with gift_list_item_id
    """
    try:
        gift_list_item = GiftListItem.objects.get(pk=gift_list_item_id)
    except GiftListItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if gift_list_item.status != 'purchased':
            gift_list_item.status = 'purchased'
        else:
            return Response("{'error':'Item already purchased', 'status':'ERROR'}", status=status.HTTP_400_BAD_REQUEST)
        gift_list_item.purchased_date = datetime.now()
        gift_list_item.save()

        return Response("{'status':'OK'}")


@api_view(['POST'])
def GiftListAdd(request, gift_list_id, gift_id):
    """
    Add gift to a gift list
    """
    try:
        gift_list = GiftList.objects.get(pk=gift_list_id)
    except GiftList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        gift = Gift.objects.get(pk=gift_id)
    except Gift.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        gift_list_item = GiftListItem.objects.get_or_create(status='available', gift=gift, gift_list=gift_list)

        return Response("{'status':'OK'}")


@api_view(['POST'])
def GiftListRemove(request, gift_list_id, gift_id):
    """
    Add gift to a gift list
    """
    try:
        gift_list = GiftList.objects.get(pk=gift_list_id)
    except GiftList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        gift = Gift.objects.get(pk=gift_id)
    except Gift.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        gift_list_item = GiftListItem.objects.get(gift=gift, gift_list=gift_list)
    except GiftListItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        gift_list_item.delete()
        return Response("{'status':'OK'}")


def Report(request, gift_list_id):
    gift_list = GiftList.objects.get(pk=gift_list_id)
    gift_list_items = GiftListItem.objects.filter(gift_list=gift_list).order_by('status')
    template = loader.get_template('weddinglist/report.html')
    context = {
        'gift_list': gift_list,
        'gift_list_items': gift_list_items,
    }
    return HttpResponse(template.render(context, request))
