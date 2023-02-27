from ..models import FinancialData
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.exceptions import ValidationError
from ..serializers import FinancialDataSerializer, FinancialDataApiRequestSerializer


class FinancialDataView(ListModelMixin, GenericViewSet):
    queryset = FinancialData.objects.all().order_by("date")
    serializer_class = FinancialDataSerializer

    def get_queryset(self):
        request = self.request.query_params.dict()
        try:
            validator = FinancialDataApiRequestSerializer(data=request)
            validator.is_valid(raise_exception=True)
        except BaseException:
            raise ValidationError(validator.errors) from None
        return self.queryset.filter(**validator.data)
