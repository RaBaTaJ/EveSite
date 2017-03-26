from django.contrib import admin
from .models import Transaction, CharacterTotalInvestment, WeeklyPayment, Statistics, PastTransactions

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Statistics)
admin.site.register(CharacterTotalInvestment)
admin.site.register(WeeklyPayment)
admin.site.register(PastTransactions)
