"""weddinglist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework import routers, viewsets
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from weddinglist.models import User
from weddinglist.serializers import UserSerializer, GiftSerializer, GiftListSerializer
from weddinglist.views import UserViewSet, GiftViewSet, GiftListViewSet, PurchaseGift, GiftListAdd, GiftListRemove, Report

# Serializers define the API representation.


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'email', 'is_staff']


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'gifts', GiftViewSet)
router.register(r'giftlists', GiftListViewSet)


favicon_view = RedirectView.as_view(
    url='/static/images/favicon.png', permanent=True)

urlpatterns = [
    path('', include(router.urls)),
    path('favicon.ico', favicon_view),
    path('purchasegift/<int:gift_list_item_id>', PurchaseGift),
    path('giftlistadd/<int:gift_list_id>/<int:gift_id>', GiftListAdd),
    path('giftlistremove/<int:gift_list_id>/<int:gift_id>', GiftListRemove),
    path('report/<int:gift_list_id>', Report),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('openapi', get_schema_view(
        title="Wedding List API",
        description="API for Wedding Lists",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
