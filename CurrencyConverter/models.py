from django.db import models


class Currency(models.Model):
    name = models.CharField(default='n/a', max_length=3)
    exchange_rate = models.FloatField()

    def __str__(self):
        return "{};{}".format(self.name, self.exchange_rate)
