import sys
import csv
import io


from django.conf import settings
import credixco.settings as app_settings

settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)

import django
django.setup()

from bank.models import Bank

with open('bank_branches.csv') as csvfile:
    data_set = csvfile.read()
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        _, created = Bank.objects.update_or_create(
            IFSCCode=column[0],
            bank_id=column[1],
            branch=column[2],
            address=column[3],
            city=column[4],
            district=column[5],
            state=column[6],
            bank_name=column[7]
        )