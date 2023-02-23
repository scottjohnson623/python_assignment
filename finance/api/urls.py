from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"financial_data", views.FinancialDataView)

urlpatterns = [
    path("", include(router.urls)),
    path("statistics", views.StatisticsView.as_view()),
]
