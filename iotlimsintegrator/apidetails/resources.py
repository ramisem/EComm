from import_export import resources, fields

from .models import ApplicationDetail, APIDetail, API_Property_Details


class ApplicationDetailResource(resources.ModelResource):
    class Meta:
        model = ApplicationDetail
        import_id_fields = ('name',)
        fields = (
            'name',
            'base_url',
        )


class APIDetailResource(resources.ModelResource):
    application_name = fields.Field(column_name='application_name', attribute='app_id__name')
    base_url = fields.Field(column_name='base_url', attribute='app_id__base_url')
    api_properties = fields.Field(column_name='api_properties')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_name_application_instance_map = {}
        self.api_name_properties_map = {}

    class Meta:
        model = APIDetail
        import_id_fields = ('name',)
        fields = (
            'name',
            'application_name',
            'base_url',
            'end_point_url',
            'type',
            'success_code',
            'authorization_property_id',
            'authorization_keyword',
            'processing_script',
            'api_properties',
        )

    def dehydrate_application_name(self, obj):
        return obj.app_id.name if obj.app_id else ''

    def dehydrate_base_url(self, obj):
        return obj.app_id.base_url if obj.app_id else ''

    def dehydrate_api_properties(self, obj):
        api_detail = APIDetail.objects.get(name=obj.name)
        if api_detail:
            api_properties = api_detail.api_property_details_set.all()
        property_details_string = ''
        if api_properties:
            for property_detail in api_properties:
                property_details_string += f",property_id:{property_detail.property_id}|property_value:{property_detail.property_value}|is_keyword:{property_detail.is_keyword}|is_url_property:{property_detail.is_url_property}"
            property_details_string = property_details_string[1:]
        return property_details_string

    def import_row(self, row, instance_loader, using_transactions=True, dry_run=False, **kwargs):
        application_name = row.get('application_name', None)
        base_url = row.get('base_url', None)
        api_properties = row.get('api_properties', None)
        application_detail_instance, created = ApplicationDetail.objects.get_or_create(name=application_name)
        if base_url:
            application_detail_instance.base_url = base_url
            application_detail_instance.save()
        self.api_name_application_instance_map[row['name']] = application_detail_instance
        if api_properties:
            self.api_name_properties_map[row['name']] = api_properties
        del row['application_name']
        del row['base_url']
        del row['api_properties']
        return super().import_row(row, instance_loader, **kwargs)

    def after_import(self, dataset, result, **kwargs):
        imported_data = dataset.dict
        for row in imported_data:
            api_detail = APIDetail.objects.get(name=row['name'])
            if api_detail:
                application_instance = self.api_name_application_instance_map.get(row['name'])
                if application_instance:
                    api_detail.app_id = application_instance
                    api_detail.save()
                api_properties = self.api_name_properties_map.get(row['name'])
                if api_properties:
                    property_sets = api_properties.split(",")

                    # Process each property set and create API_Property_Details instances
                    for property_set in property_sets:
                        properties = property_set.split("|")
                        prop_dict = {}
                        for prop in properties:
                            prop_name, prop_value = prop.split(":")
                            prop_dict[prop_name.strip()] = prop_value.strip() if prop_value.strip() != "None" else None

                        existing_property = API_Property_Details.objects.filter(api_detail_id=api_detail,
                                                                                property_id=prop_dict.get(
                                                                                    "property_id")).first()

                        if existing_property:
                            # Update the existing API_Property_Details instance
                            existing_property.property_value = prop_dict.get("property_value")
                            existing_property.is_keyword = prop_dict.get("is_keyword")
                            existing_property.is_url_property = prop_dict.get("is_url_property")
                            existing_property.save()
                        else:
                            # Create a new API_Property_Details instance
                            api_property = API_Property_Details.objects.create(
                                api_detail_id=api_detail,
                                property_id=prop_dict.get("property_id"),
                                property_value=prop_dict.get("property_value"),
                                is_keyword=prop_dict.get("is_keyword"),
                                is_url_property=prop_dict.get("is_url_property")
                            )
                            api_property.save()

        return super().after_import(dataset, result, **kwargs)

