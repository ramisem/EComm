import datetime

from admin_tools_stats.forms import ChartSettingsForm
from admin_tools_stats.models import DashboardStats, Interval, get_charts_timezone, CriteriaToStatsM2M
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from typing import List, Mapping, Optional, Union

from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q
from django.db.models.functions import Trunc
from django.db.models import Value, DateTimeField


class CustomDashboardStats(DashboardStats):
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = 'Dashboard'

    def get_date_field(self):
        query = self.get_queryset().all().query
        if 'all' == self.date_field_name:
            return 'all'
        return query.resolve_ref(self.date_field_name).field

    def get_time_series(
            self,
            dynamic_criteria: Mapping[str, Union[str, List[str]]],
            all_criteria: List["CriteriaToStatsM2M"],
            user: Union[User, AnonymousUser],
            time_since: datetime.datetime,
            time_until: datetime.datetime,
            operation_choice: Optional[str],
            operation_field_choice: Optional[str],
            interval: Interval,
    ):
        """Get the stats time series"""
        kwargs = {}
        dynamic_kwargs: List[Optional[Q]] = []
        if not user.has_perm("admin_tools_stats.view_dashboardstats") and self.user_field_name:
            kwargs[self.user_field_name] = user
        for m2m in all_criteria:
            criteria = m2m.criteria
            if criteria.criteria_fix_mapping:
                for key in criteria.criteria_fix_mapping:
                    kwargs[key] = criteria.criteria_fix_mapping[key]

            dynamic_key = "select_box_dynamic_%i" % m2m.id
            if dynamic_key in dynamic_criteria:
                if dynamic_criteria[dynamic_key] != "":
                    dynamic_values = dynamic_criteria[dynamic_key]
                    dynamic_field_name = m2m.get_dynamic_criteria_field_name()
                    criteria_key = "id" if dynamic_field_name == "" else dynamic_field_name
                    if isinstance(dynamic_values, (list, tuple)):
                        single_value = False
                    elif isinstance(dynamic_values, str):
                        dynamic_values = [
                            dynamic_values,
                        ]
                        single_value = True

                    for dynamic_value in dynamic_values:
                        try:
                            criteria_value = m2m.get_dynamic_choices(
                                time_since,
                                time_until,
                                operation_choice,
                                operation_field_choice,
                                user,
                            )[dynamic_value]
                        except KeyError:
                            criteria_value = 0
                        if isinstance(criteria_value, (list, tuple)):
                            criteria_value = criteria_value[0]
                        else:
                            criteria_value = dynamic_value
                        criteria_key_string = criteria_key + (
                            "__in" if isinstance(criteria_value, list) else ""
                        )
                        if single_value:
                            kwargs[criteria_key_string] = criteria_value
                        else:
                            dynamic_kwargs.append(Q(**{criteria_key_string: criteria_value}))

        aggregate_dict = {}
        i = 0
        if not dynamic_kwargs:
            dynamic_kwargs = [None]

        operations = self.get_operations_list()
        if operations and len(operations) > 1 and operation_choice == "":
            for operation in operations:
                i += 1
                aggregate_dict["agg_%i" % i] = self.get_operation(operation_choice, operation)
        else:
            for dkwargs in dynamic_kwargs:
                i += 1
                aggregate_dict["agg_%i" % i] = self.get_operation(
                    operation_choice, operation_field_choice, dkwargs
                )

        qs = self.get_queryset()
        if isinstance(self.get_date_field(), DateTimeField):
            time_range = {"%s__range" % self.date_field_name: (time_since, time_until)}
            qs = qs.filter(**time_range)
        qs = qs.filter(**kwargs)
        if isinstance(self.get_date_field(), DateTimeField):
            tzinfo_kwargs = {"tzinfo": get_charts_timezone()}
            qs = qs.annotate(d=Trunc(self.date_field_name, interval.val(), **tzinfo_kwargs))
        else:
            qs = qs.annotate(d=Value(None, output_field=DateTimeField()))
        qs = qs.values_list("d")
        qs = qs.order_by("d")
        qs = qs.annotate(**aggregate_dict)
        return qs

    def get_control_form_raw(self, user=None):
        print('custom_get_control_form_raw')
        if isinstance(self.get_date_field(), DateTimeField):
            return ChartSettingsForm(self, user, auto_id=False)
        else:
            from dashboard.forms import CustomChartSettingsForm
            return CustomChartSettingsForm(self, user, auto_id=False)


auditlog.register(CustomDashboardStats)
