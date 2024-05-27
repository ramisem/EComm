from django.urls import path

from dashboard import views
from dashboard.views import CustomAdminChartsView
from dashboard.views import CustomChartDataView, CustomAnalyticsChartView

app_name = 'dashboard'


class URLS:
    urlpatterns = [
        path('ajax/get_model_names/', views.get_model_names,
             name='get_model_names'),
        path('ajax/get_date_and_operation_field_names/', views.get_date_and_operation_field_names,
             name='get_date_and_operation_field_names'),
        path("customanalytics/", views.CustomAnalyticsView.as_view(), name="custom_chart-analytics"),
        path(
            "custom_chart_data/", CustomChartDataView.as_view(), name="custom-chart-data"
        ),
        path("custom_chart_data/<str:graph_key>/", CustomChartDataView.as_view(), name="custom-chart-data"),
        path(
            "analytics/chart/",
            CustomAnalyticsChartView.as_view(),
            name="custom-chart-analytics-without-key",
        ),
        path(
            "admin_charts.js",
            CustomAdminChartsView.as_view(content_type="application/javascript"),
            name="custom-admin-charts",
        ),
    ]

    def __dir__(self):
        return self.urlpatterns
