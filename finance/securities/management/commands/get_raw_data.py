from django.conf import settings
from datetime import date
from django.core.management.base import BaseCommand
from securities.models import FinancialData
from ...serializers import FinancialDataSerializer
import requests


class Command(BaseCommand):
    help = "Import stock data from Alphavantage to seed database"

    def handle(self, *args, **options):
        api_key = settings.ALPHAVANTAGE_API_KEY
        if not api_key:
            raise Exception(
                "Unable to locate ALPHAVANTAGE_API_KEY. Please make sure it is in your .env and try again."
            )
        symbols = ["IBM", "AAPL"]
        date_cutoff_in_days = 14
        current_date = date.today()
        new_financial_data_models = []

        for symbol in symbols:
            request = requests.get(
                f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={settings.ALPHAVANTAGE_API_KEY}"
            ).json()
            json_data = request["Time Series (Daily)"]
            for day in json_data:
                if (current_date - date.fromisoformat(day)).days >= date_cutoff_in_days:
                    break
                day_data = json_data[day]

                validator = FinancialDataSerializer(
                    data={
                        "date": day,
                        "symbol": symbol,
                        "open_price": day_data["1. open"],
                        "close_price": day_data["4. close"],
                        "volume": day_data["6. volume"],
                    }
                )
                try:
                    validator.is_valid(raise_exception=True)
                    new_financial_data_models.append(
                        FinancialData(**validator.validated_data)
                    )
                except:
                    print(
                        f"there was a problem with the data from {day}: {validator.errors}. Skipping adding to database"
                    )

        FinancialData.objects.bulk_create(
            new_financial_data_models, ignore_conflicts=True
        )
        self.stdout.write(
            self.style.SUCCESS("Finished importing data from Alphavantage API")
        )
