from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin

from ..models import Order, OrderItem


class OrderItemInlineAdmin(BaseTabularInline, MembershipBaseModelAdmin):
    model = OrderItem
    fields = ('aliquot', 'panel', 'order_datetime', 'order_identifier', 'subject_identifier')
    readonly_fields = ('aliquot', 'order_identifier', 'subject_identifier')


class OrderItemAdmin(MembershipBaseModelAdmin):

    fields = ('aliquot', 'panel', 'order_datetime', 'order_identifier', 'subject_identifier')
    list_display = ('order_identifier', 'aliquot', 'panel', 'order_datetime', 'subject_identifier')
    search_fields = ('id', 'order__id', 'order_identifier', 'aliquot__aliquot_identifier',
                     'subject_identifier')
    readonly_fields = ('aliquot', 'order_identifier', 'subject_identifier')

admin.site.register(OrderItem, OrderItemAdmin)


class OrderAdmin(MembershipBaseModelAdmin):

    list_display = ('id', 'order_datetime', 'items')
    list_filter = ("order_datetime", )
    search_fields = ('id', )
    inlines = [OrderItemInlineAdmin, ]

admin.site.register(Order, OrderAdmin)
