from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
import time

class ExpenseType(models.Model):
    expense_name = models.CharField(max_length=250, null=False)
    default = models.BooleanField(default=False)
    default_order = models.IntegerField(null=True, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='expense_type_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='expense_updated_by')

    class Meta:
        ordering = ('id',)


    def __unicode__(self):
        return '%s:%s:%s'%(self.expense_name, self.default, self.default_order)

    def get_default_expense_item_obj(self, price, dollar_rate, commission, currency='PKR'):

        name = self.expense_name.replace('%price%', price).replace('%dollarRate%', dollar_rate)\
            .replace('%commission%', commission).replace('%currency%', currency)
        return {
            'name': name,
            'amount': 0.00
        }


    @classmethod
    def populate_empty_table(cls):

        charges = [
            ('Bank Charges', True, 1),
            ('Indenting Commission + Adjustment', True, 2),
            ('Pay Order Collector of Custom', True, 3),
            ('Pay Order Excise & Taxation Office', True, 2),
            ('Pay Order Wharfage', True, 2),
            ('Pay Order Terminal Handling Charges', True, 2),
            ('Endorsment Charges', True, 2),
            ('Documents ( $ %commission% * %currency% %dollarRate%)', True, 2),
            ('L/C Fees', True, 2),
            ('Insurance', True, 2),
            ('Market Fees', True, 2),
            ('Import Permit', True, 2),
            ('LC Form', True, 2),
            ('Demurrage Charges', True, 2),
            ('Detention Charges', True, 2),
            ('SGS Charges', True, 2),
            ('Godown/Warehouse Charges', True, 2),
            ('Packing Charges', True, 2),
            ('UN Loading', True, 2),
            ('Lolo Charges', True, 2),
            ('Clearing Charges', True, 2)
        ]

        count = cls.objects.count()
        u = User.objects.get(username='immadimtiaz')

        if not count:
            for charge in charges:
                new_expense_type = cls()
                new_expense_type.expense_name = charge[0]
                new_expense_type.default = charge[1]
                new_expense_type.default_order = charge[2]
                new_expense_type.created_by = u
                new_expense_type.save()





