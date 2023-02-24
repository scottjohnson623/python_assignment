from django.conf import settings
from datetime import date
from django.core.management.base import BaseCommand
from api.models import FinancialData
from ...serializers import FinancialDataSerializer
import requests


class Command(BaseCommand):
    help = "Import stock data from Alphavantage to seed database"

    def handle(self, *args, **options):
        symbols = ["IBM", "AAPL"]

        current_date = date.today()
        new_financial_data_models = []

        for symbol in symbols:
            request = requests.get(
                f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={settings.ALPHAVANTAGE_API_KEY}"
            ).json()
            json_data = request["Time Series (Daily)"]
            for day in json_data:
                if (current_date - date.fromisoformat(day)).days >= 14:
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
                        f"there was a problem with the data from {day}: {validator.errors}"
                    )

        FinancialData.objects.bulk_create(
            new_financial_data_models, ignore_conflicts=True
        )
        self.stdout.write(
            self.style.SUCCESS("Finished importing data from Alphavantage API")
        )
