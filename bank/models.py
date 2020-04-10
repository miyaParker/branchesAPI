from django.db import models

# Create your models here.


class Branch(models.Model):
    IFSCCode = models.CharField(
        max_length=11, unique=True, primary_key=True, null=False)
    bank_id = models.IntegerField()
    branch = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=200,)
    city = models.CharField(max_length=50, null=False)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=30, null=False)
    bank_name = models.CharField(
        max_length=50, verbose_name='bank-name')

    def __str__(self):
        return self.bank_name + self.IFSCCode
