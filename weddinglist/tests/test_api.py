import pytest
import json

from rest_framework.test import RequestsClient
from weddinglist.models import User, Gift, GiftList, GiftListItem

pytestmark = pytest.mark.django_db


class TestUser:
    def test_create_user(self):
        active_user = User.objects.create_user(email='active_user@example.com', password='pass')
        assert User.objects.filter(id=active_user.id).exists()


class TestGiftList:

    def test_create_gift(self):
        gift = Gift.objects.create(name="Surprise", brand="Best")
        assert Gift.objects.filter(id=gift.id).exists()


class TestApi:

    def test_api(self):
        # GIVEN
        Gift.objects.create(name="Surprise", brand="Best")
        client = RequestsClient()
        # WHEN
        response = client.get('http://127.0.0.1:8000/gifts/?format=json')
        # THEN
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
