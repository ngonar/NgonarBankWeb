from django.db import models

# Create your models here.
class BankAccount(models.Model):
    account_no = models.CharField(max_length=15)
    account_name = models.CharField(max_length=32)
    account_balance = models.IntegerField()

    def __str__(self):
        return self.account_no + " - " + self.account_name + " - " + str(self.account_balance)