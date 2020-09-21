import re
from datetime import date, timedelta

import requests
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.utils.html import strip_tags
from rest_framework import permissions, viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend

# from weddinglist.models import Pokemon
from weddinglist.serializers import (UserSerializer, GroupSerializer,
                                     GiftSerializer,
                                     GiftListSerializer,)
from weddinglist.models import Gift, GiftList, User


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
