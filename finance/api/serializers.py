from .models import FinancialData
from rest_framework import serializers


class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = ["symbol", "date", "open_price", "close_price", "volume"]


class FinancialDataApiRequestSerializer(serializers.Serializer):
    symbol = serializers.CharField(min_length=1, max_length=12, required=False)
    start_date = serializers.DateField(allow_null=True, required=False)
    end_date = serializers.DateField(allow_null=True, required=False)

    def to_representation(self, instance):
        dict = {}
        if "symbol" in instance:
            dict["symbol"] = instance["symbol"]
        if "start_date" in instance:
            dict["date__gte"] = instance["start_date"]
        if "end_date" in instance:
            dict["date__lte"] = instance["end_date"]
        return dict


class StatisticsApiRequestSerializer(serializers.Serializer):
    symbol = serializers.CharField(min_length=1, max_length=12, required=False)
    start_date = serializers.DateField(allow_null=True)
    end_date = serializers.DateField(allow_null=True)

    def to_representation(self, instance):
        return {
            "symbol": instance["symbol"],
            "date__range": [instance["start_date"], instance["end_date"]],
        }
