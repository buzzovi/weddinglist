from django.contrib.auth.models import Group
from rest_framework import serializers

from weddinglist.models import Gift, GiftList, GiftListItem, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'email', 'groups', 'is_staff']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = ['id', 'name', 'created', 'modified', ]


class GiftListItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GiftListItem
        fields = ['id', 'gift', 'status', 'purchased_date', ]


class GiftListSerializer(serializers.HyperlinkedModelSerializer):
    giftlist = GiftListItemSerializer(many=True, read_only=True)

    class Meta:
        model = GiftList
        fields = ['id', 'name', 'created', 'modified', 'giftlist', ]
