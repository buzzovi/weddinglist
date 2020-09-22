from django.contrib import admin
from django.forms.models import BaseInlineFormSet
# from django.utils.translation import ugettext_lazy as _

from weddinglist.models import User, Gift, GiftList, GiftListItem


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    fieldsets = (
        (None, {'fields': (
                'email', 'first_name', 'last_name',)
                }),
        # (_('Language'), {'fields': ('lang', )}),
    )

    list_display = ('pk', 'email')
    search_fields = ('email',)
    list_filter = ('is_staff', )


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    fieldsets = (
        (None, {'fields': (
                'name', 'brand', 'price', 'currency', 'in_stock_quantity', 'info',)
                }),
        # (_('Language'), {'fields': ('lang', )}),
    )

    list_display = ('pk', 'name', 'brand', 'price', 'currency', 'in_stock_quantity')
    search_fields = ('name',)
    list_filter = ('brand', )


class GiftListItemInlineFormSet(BaseInlineFormSet):
    def save_new_objects(self, form, commit=True):
        saved_instances = super().save_new_objects(commit)
        if commit:
            for instance in saved_instances:
                if instance.gift_list_id is not None:
                    # GiftList a = GiftList.objects.get(id=instance.id)
                    # instance.gift_list_id = a.id
                    pass
        return saved_instances


class GiftListItemInline(admin.TabularInline):
    model = GiftListItem
    extra = 0
    fromset = GiftListItemInlineFormSet
    readonly_fields = ('created', 'modified', 'status', 'price',)
    fields = ['gift',  'status', 'price', ]

    def price(self, obj):
        return obj.gift.price
    price.short_description = 'Price'
    price.admin_order_field = 'gift__price'


@admin.register(GiftList)
class GiftListAdmin(admin.ModelAdmin):
    inlines = [GiftListItemInline, ]
    readonly_fields = ('created', 'modified')
    fieldsets = (
        (None, {'fields': (
                'name', )
                }),
        # (_('Language'), {'fields': ('lang', )}),
    )

    list_display = ('pk', 'name',)
    search_fields = ('name',)
