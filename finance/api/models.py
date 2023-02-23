from django.db import models


class FinancialData(models.Model):
    class Meta:
        db_table = "financial_data"
        indexes = [
            models.Index(
                fields=[
                    "symbol",
                ]
            ),
            models.Index(
                fields=[
                    "date",
                ]
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "symbol",
                    "date",
                ],
                name="unique_symbol_date",
            )
        ]

    symbol = models.CharField(max_length=6)
    date = models.DateField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.PositiveBigIntegerField()
