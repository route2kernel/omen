from CurrencyConverter.models import Currency
from django.core.management.base import BaseCommand, CommandError
import defusedxml.ElementTree as ET
import requests


class Command(BaseCommand):
    help = 'Remplir ou mettre à jour la base de données avec les taux de change depuis https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'

    def handle(self, *args, **options):
        try:
            request = requests.get("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
            response = request.text
        except (requests.RequestException, requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
            raise CommandError(e)

        try:
            root = ET.fromstring(response)
        except ET.ParseError as e:
            raise CommandError(e)

        found_curr = 0
        for element in root.iter():
            curr_name = element.get('currency')
            curr_rate = element.get('rate')
            if(curr_name is not None and curr_rate is not None):
                found_curr += 1
                try:
                    currency = Currency.objects.get(name=curr_name)
                    currency.exchange_rate = curr_rate
                    currency.save()
                except Currency.DoesNotExist:
                    currency = Currency(name=curr_name, exchange_rate=float(curr_rate))
                    currency.save()
        if found_curr != 0:
            self.stdout.write(
                self.style.SUCCESS('Successfully fetched {} exchange rates and updated the database.'.format(found_curr))
            )
        else:
            raise CommandError("Found 0 corresponding elements!")
