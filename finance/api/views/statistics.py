from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from ..models import FinancialData
from ..serializers import FinancialDataSerializer, StatisticsApiRequestSerializer


class StatisticsView(APIView):
    queryset = FinancialData.objects.all().order_by("date")
    serializer_class = FinancialDataSerializer

    def get(self, request, format=None):
        try:
            validator = StatisticsApiRequestSerializer(data=request.query_params.dict())
            validator.is_valid(raise_exception=True)
        except BaseException:
            raise ValidationError(validator.errors) from None
        data = FinancialData.objects.filter(**validator.data).aggregate(
            open_price=Avg("open_price"),
            close_price=Avg("close_price"),
            volume=Avg("volume"),
        )
        data.update(validator.initial_data)
        return Response({"data": data})
