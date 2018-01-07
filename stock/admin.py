from django.contrib import admin

# Register your models here.
from .models import Stock, StockValues, Profile

admin.site.register(Profile)
admin.site.register(Stock)
admin.site.register(StockValues)