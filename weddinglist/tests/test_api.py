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

    def test_gift_api(self):
        # GIVEN
        Gift.objects.create(name="Surprise", brand="Best")
        client = RequestsClient()
        # WHEN
        response = client.get('http://127.0.0.1:8000/gifts/?format=json')
        # THEN
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_gift_list_api(self):
        # GIVEN
        GiftList.objects.create(name="Surprise")
        client = RequestsClient()
        # WHEN
        response = client.get('http://127.0.0.1:8000/giftlists/?format=json')
        # THEN
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_purchasegift_api(self):
        # GIVEN
        gift_list = GiftList.objects.create(name="Surprise")
        gift = Gift.objects.create(name="Surprise", brand="Best")
        gift_list_item = GiftListItem.objects.create(gift=gift, gift_list=gift_list)
        client = RequestsClient()
        # WHEN
        response = client.post('http://127.0.0.1:8000/purchasegift/'+str(gift_list_item.id))
        # THEN
        assert response.status_code == 200
        assert json.loads(response.content) == "{'status':'OK'}"

    def test_giftlistadd_api(self):
        # GIVEN
        gift_list = GiftList.objects.create(name="Surprise")
        gift = Gift.objects.create(name="Surprise", brand="Best")
        client = RequestsClient()
        # WHEN
        response = client.post(f'http://127.0.0.1:8000/giftlistadd/{gift_list.id}/{gift.id}')
        # THEN
        assert response.status_code == 200
        assert json.loads(response.content) == "{'status':'OK'}"

    def test_giftlistremove_api(self):
        # GIVEN
        gift_list = GiftList.objects.create(name="Surprise")
        gift = Gift.objects.create(name="Surprise", brand="Best")
        GiftListItem.objects.create(gift=gift, gift_list=gift_list)
        client = RequestsClient()
        # WHEN
        response = client.post(f'http://127.0.0.1:8000/giftlistremove/{gift_list.id}/{gift.id}')
        # THEN
        assert response.status_code == 200
        assert json.loads(response.content) == "{'status':'OK'}"

    def test_report(self):
        # GIVEN
        gift_list = GiftList.objects.create(name="Surprise")
        gift = Gift.objects.create(name="Surprise", brand="Best")
        GiftListItem.objects.create(gift=gift, gift_list=gift_list)
        client = RequestsClient()
        # WHEN
        response = client.get('http://127.0.0.1:8000/report/1')
        # THEN
        assert response.status_code == 200
