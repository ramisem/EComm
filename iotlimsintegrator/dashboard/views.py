import logging
import time
from collections import OrderedDict
from datetime import datetime
from typing import Dict, List, Optional, Union

from admin_tools_stats.models import truncate_ceiling
from admin_tools_stats.views import AnalyticsView, remove_multiple_keys, get_dateformat, ChartsMixin
from datetime_truncate import truncate
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import JsonResponse
from django.views.generic import TemplateView

from dashboard.models import CustomDashboardStats
from .models import Interval, get_charts_timezone

logger = logging.getLogger(__name__)


def get_model_names(request):
    try:
        app_name = request.GET.get('app_name', None)
        app_config = apps.get_app_config(app_name)
        model_data = [
            {'model_name': model.__name__, 'verbose_name': model._meta.verbose_name}
            for model in app_config.get_models()
        ]
        return JsonResponse({'model_data': model_data})
    except LookupError:
        return JsonResponse({'error': 'App not found'}, status=404)


def get_date_and_operation_field_names(request):
    try:
        app_name = request.GET.get('app_name', None)
        model_name = request.GET.get('model_name', None)
        model = apps.get_model(app_name, model_name)
        datetime_fields = [
            {'field_name': field.name, 'verbose_name': field.verbose_name}
            for field in model._meta.get_fields()
            if isinstance(field, models.Field) and isinstance(field, models.DateTimeField)
        ]
        operation_fields = [
            {'field_name': field.name, 'verbose_name': field.verbose_name}
            for field in model._meta.get_fields()
            if
            isinstance(field, models.Field) and not isinstance(field, models.DateTimeField) and field.name != 'history'
        ]
        datetime_fields.append({'field_name': 'all', 'verbose_name': 'All'})
        return JsonResponse({'datetime_fields': datetime_fields, 'operation_fields': operation_fields})
    except LookupError:
        return JsonResponse({'error': 'Model not found'}, status=404)


class CustomAnalyticsView(AnalyticsView):
    def get_template_names(self):
        if self.request.user.has_perm("admin_tools_stats.view_dashboardstats"):
            return "admin/dashboard/analytics.html"
        return "admin_tools_stats/analytics_user.html"


class CustomAdminChartsView(TemplateView):
    template_name = "admin/dashboard/admin_charts.js"


class CustomChartDataView(TemplateView):
    template_name = "admin_tools_stats/chart_data.html"

    def get_context_data(
            self, *args, interval: Optional[Interval] = None, graph_key=None, **kwargs
    ):
        dashboard_stats = CustomDashboardStats.objects.get(graph_key=graph_key)
        context = super().get_context_data(*args, **kwargs)

        if not (
                self.request.user.has_perm("admin_tools_stats.view_dashboardstats")
                or dashboard_stats.show_to_users
        ):
            context["error"] = (
                "You have no permission to view this chart. "
                "Check if you are logged in and have permission "
                "'admin_tools_stats | dashboard stats | Can view dashboard stats'"
            )
            context["graph_title"] = dashboard_stats.graph_title
            return context

        dict = self.request.GET
        configuration: Dict[str, Union[str, List[str]]] = {item: dict[item] for item in dict}
        remove_multiple_keys(configuration, ["csrfmiddlewaretoken", "_", "graph_key"])
        if dashboard_stats.date_field_name == 'all':
            selected_interval: Interval = Interval(
                'years'
            )
        else:
            selected_interval: Interval = Interval(
                configuration.pop("select_box_interval", interval) or dashboard_stats.default_time_scale
            )
        operation = configuration.pop(
            "select_box_operation", dashboard_stats.type_operation_field_name
        )
        if not isinstance(operation, str):
            operation = None
        operation_field = configuration.pop(
            "select_box_operation_field", dashboard_stats.operation_field_name
        )
        if not isinstance(operation_field, str):
            operation_field = None
        context["chart_type"] = configuration.pop(
            "select_box_chart_type", dashboard_stats.default_chart_type
        )
        try:
            chart_tz = get_charts_timezone()
            try:
                time_since = datetime.strptime(str(configuration.pop("time_since")), "%Y-%m-%d")
            except KeyError:
                time_since = datetime.today()
            time_since = truncate(time_since, selected_interval.val())
            time_since = time_since.astimezone(chart_tz)

            try:
                time_until = datetime.strptime(str(configuration.pop("time_until")), "%Y-%m-%d")
            except KeyError:
                time_until = datetime.today()
            time_until = truncate_ceiling(time_until, selected_interval.val())
            time_until = time_until.astimezone(chart_tz)

            if time_since > time_until:
                context["error"] = "Time since is greater than time until"
                context["graph_title"] = dashboard_stats.graph_title
                return context

            if dashboard_stats.cache_values:
                get_time_series = dashboard_stats.get_multi_time_series_cached
            else:
                get_time_series = dashboard_stats.get_multi_time_series

            series = get_time_series(
                configuration,
                time_since,
                time_until,
                selected_interval,
                operation,
                operation_field,
                self.request.user,
            )
        except Exception as e:
            if "debug" in configuration:
                raise e
            context["error"] = str(e)
            context["graph_title"] = dashboard_stats.graph_title
            logger.exception(e)
            return context

        ydata_serie: Dict[str, List[int]] = {}
        names = {}
        xdata = []
        serie_i_map: Dict[str, int] = OrderedDict()
        for date in sorted(
                series.keys(),
                key=lambda d: datetime.now() if d is None else datetime(d.year, d.month, d.day, getattr(d, "hour", 0)),
                reverse=True if dashboard_stats.date_field_name == 'all' else False
        ):
            if date is None:
                current_datetime = datetime.now()
                timestamp = int(time.mktime(current_datetime.timetuple()) * 1000)
            else:
                timestamp = int(time.mktime(date.timetuple()) * 1000)

            xdata.append(timestamp)

            for key, value in series[date].items():
                if key not in serie_i_map:
                    serie_i_map[key] = len(serie_i_map)
                y_key = "y%i" % serie_i_map[key]
                if y_key not in ydata_serie:
                    ydata_serie[y_key] = []
                    names["name%i" % serie_i_map[key]] = str(key)
                if dashboard_stats.date_field_name == 'all':
                    if value:
                        ydata_serie[y_key].append(value)
                else:
                    ydata_serie[y_key].append(value if value else 0)

        context["extra"] = {
            "x_is_date": True,
            "tag_script_js": False,
        }

        if dashboard_stats.y_axis_format:
            context["extra"]["y_axis_format"] = dashboard_stats.y_axis_format

        if context["chart_type"] == "stackedAreaChart":
            context["extra"]["use_interactive_guideline"] = True

        tooltip_date_format, context["extra"]["x_axis_format"] = get_dateformat(
            selected_interval, context["chart_type"]
        )

        extra_serie = {
            "tooltip": {"y_start": "", "y_end": ""},
            "date_format": tooltip_date_format,
        }

        context["values"] = {
            "x": xdata,
            "name1": selected_interval,
            **ydata_serie,
            **names,
            "extra1": extra_serie,
        }

        context["chart_container"] = "chart_container_" + graph_key
        return context


class CustomAnalyticsChartView(LoginRequiredMixin, ChartsMixin, TemplateView):
    template_name = "admin/dashboard/analytics_chart.html"

    def get_context_data(self, *args, graph_key=None, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if graph_key is None:
            graph_key = self.request.GET.get('graph_key')
        dashboard_stats = CustomDashboardStats.objects.get(graph_key=graph_key)
        if dashboard_stats.date_field_name == 'all':
            context_data["all"] = "Y"
        context_data["chart"] = self.get_charts_query().get(graph_key=graph_key)
        return context_data

    def get_charts_query(self):
        query = CustomDashboardStats.objects.order_by("graph_title").all()
        if not self.request.user.has_perm("admin_tools_stats.view_dashboardstats"):
            query = query.filter(show_to_users=True)
        return query
