from django.contrib import admin
from .models import DepositOptions, DepositProducts, SavingOptions, SavingProducts, DepositSubscription, SavingSubscription

admin.site.register(DepositOptions)
admin.site.register(DepositProducts)
admin.site.register(SavingOptions)
admin.site.register(SavingProducts)
admin.site.register(DepositSubscription)
admin.site.register(SavingSubscription)
