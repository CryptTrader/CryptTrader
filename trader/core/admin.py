from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BillingAccount, BTCOrder, BTCSellOrder, BTCBuyOrder, User, FundsTransfer


def execute_order(_, request, queryset):
    del request  # Not used
    queryset.update(order_state='EXECUTED')


def cancel_order(_, request, queryset):
    del request  # Not used
    queryset.update(order_state='CANCELLED')


class BillingAccountModelAdmin(admin.ModelAdmin):
    list_display = 'username', 'balance_brl', 'balance_btc', 'active', 'created_at'
    search_fields = 'user.username', 'active'

    def username(self, obj):
        return obj.user.username


class BTCOrderModelAdmin(admin.ModelAdmin):
    list_display = 'username', 'type', 'amount_brl', 'amount_btc', 'exchange_rate', \
                   'order_state', 'is_executed', 'created_at'
    list_filter = 'type', 'order_state'
    search_fields = 'state',
    date_hierarchy = 'created_at'
    actions_on_bottom = True
    actions = [execute_order, cancel_order]

    def username(self, obj):
        return obj.billing_account.user.username

    def is_executed(self, obj):
        return obj.order_state == 'EXECUTED'

    is_executed.boolean = True
    execute_order.boolean = True
    execute_order.short_description = 'Execute Orders'
    cancel_order.short_description = 'Cancel Orders'


class BTCBuyOrderModelAdmin(BTCOrderModelAdmin):
    list_display = 'username', 'amount_brl', 'amount_btc', 'exchange_rate', 'order_state', 'created_at'


class BTCSellOrderModelAdmin(BTCOrderModelAdmin):
    list_display = 'username', 'amount_brl', 'amount_btc', 'exchange_rate', 'order_state', 'created_at'


class FundsTransferModelAdmin(admin.ModelAdmin):
    list_display = 'username', 'amount_brl', 'is_executed', 'funds_transfer_state', 'created_at'
    search_fields = 'state',
    date_hierarchy = 'created_at'
    actions_on_bottom = True

    def username(self, obj):
        return obj.billing_account.user.username

    def is_executed(self, obj):
        return obj.funds_transfer_state == 'EXECUTED'

    is_executed.boolean = True


admin.site.register(BillingAccount, BillingAccountModelAdmin)
admin.site.register(BTCOrder, BTCOrderModelAdmin)
admin.site.register(BTCSellOrder, BTCSellOrderModelAdmin)
admin.site.register(BTCBuyOrder, BTCBuyOrderModelAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(FundsTransfer, FundsTransferModelAdmin)
