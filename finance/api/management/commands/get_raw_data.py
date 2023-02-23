from django.conf import settings
from datetime import date
from django.core.management.base import BaseCommand
from api.models import FinancialData
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
                open_price = float(day_data["1. open"])
                close_price = float(day_data["4. close"])
                volume = int(day_data["6. volume"])
                financial_data_model = FinancialData(
                    symbol=symbol,
                    date=day,
                    open_price=open_price,
                    close_price=close_price,
                    volume=volume,
                )
                print(financial_data_model)
                new_financial_data_models.append(financial_data_model)

        FinancialData.objects.bulk_create(
            new_financial_data_models, ignore_conflicts=True
        )
