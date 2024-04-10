(function ($) {
    'use strict';

    function FixSelectorHeight() {
        $('.selector .selector-chosen').each(function () {
            let selector_chosen = $(this);
            let selector_available = selector_chosen.siblings('.selector-available');

            let selector_chosen_select = selector_chosen.find('select').first();
            let selector_available_select = selector_available.find('select').first();
            let selector_available_filter = selector_available.find('p.selector-filter').first();

            selector_chosen_select.height(selector_available_select.height() + selector_available_filter.outerHeight());
            selector_chosen_select.css('border-top', selector_chosen_select.css('border-bottom'));
        });
    }

    function handleCarousel($carousel) {
        const errors = $('.errorlist li', $carousel);
        const hash = document.location.hash;

        // If we have errors, open that tab first
        if (errors.length) {
            const errorCarousel = errors.eq(0).closest('.carousel-item');
            $carousel.carousel(errorCarousel.data('carouselid'));
            $('.carousel-fieldset-label', $carousel).text(errorCarousel.data()["label"]);
        } else if (hash) {
            // If we have a tab hash, open that
            const activeCarousel = $('.carousel-item[data-target="' + hash + '"]', $carousel);
            $carousel.carousel(activeCarousel.data()["carouselid"]);
            $('.carousel-fieldset-label', $carousel).text(activeCarousel.data()["label"]);
        }

        // Update page hash/history on slide
        $carousel.on('slide.bs.carousel', function (e) {

            FixSelectorHeight();
            // call resize in change view after tab switch
            window.dispatchEvent(new Event('resize'));

            if (e.relatedTarget.dataset.hasOwnProperty("label")) {
                $('.carousel-fieldset-label', $carousel).text(e.relatedTarget.dataset.label);
            }
            const hash = e.relatedTarget.dataset.target;

            if (history.pushState) {
                history.pushState(null, null, hash);
            } else {
                location.hash = hash;
            }
        });
    }

    function handleTabs($tabs) {
        const errors = $('.change-form .errorlist li');
        const hash = document.location.hash;

        // If we have errors, open that tab first
        if (errors.length) {
            const tabId = errors.eq(0).closest('.tab-pane').attr('id');
            $('a[href="#' + tabId + '"]').tab('show');
        } else if (hash) {
            // If we have a tab hash, open that
            $('a[href="' + hash + '"]', $tabs).tab('show');
        }

        // Change hash for page-reload
        $('a', $tabs).on('shown.bs.tab', function (e) {

            FixSelectorHeight();
            // call resize in change view after tab switch
            window.dispatchEvent(new Event('resize'));

            e.preventDefault();
            if (history.pushState) {
                history.pushState(null, null, e.target.hash);
            } else {
                location.hash = e.target.hash;
            }
        });
    }

    function handleCollapsible($collapsible) {
        const errors = $('.errorlist li', $collapsible);
        const hash = document.location.hash;

        // If we have errors, open that tab first
        if (errors.length) {
            $('.panel-collapse', $collapsible).collapse('hide');
            errors.eq(0).closest('.panel-collapse').collapse('show');

        } else if (hash) {
            // If we have a tab hash, open that
            $('.panel-collapse', $collapsible).collapse('hide');
            $(hash, $collapsible).collapse('show');
        }

        // Change hash for page-reload
        $collapsible.on('shown.bs.collapse', function (e) {

            FixSelectorHeight();
            // call resize in change view after tab switch
            window.dispatchEvent(new Event('resize'));

            if (history.pushState) {
                history.pushState(null, null, '#' + e.target.id);
            } else {
                location.hash = '#' + e.target.id;
            }
        });
    }

    function applySelect2() {
        const noSelect2 = '.empty-form select, .select2-hidden-accessible, .selectfilter, .selector-available select, .selector-chosen select, select[data-autocomplete-light-function=select2]';
        $('select').not(noSelect2).select2({ width: 'element' });
        getParamIdsByEventIOTMapId();
    }


    function getParamIdsByEventIOTMapId() {
        const event_iot_map_id_obj = document.querySelector('#id_event_iot_map_id');
        if (typeof event_iot_map_id_obj == 'undefined' || event_iot_map_id_obj == null) {
            console.error('Event_Type_IOT_Type_Map  Object cannot be obtained.');
            return;
        }
        const event_iot_map_id = event_iot_map_id_obj.value;

        var last_col_id = '';
        for (var i = 0; true; i++) {
            var col_id = '#id_event_rule_params_set-' + i + '-param_id';
            if (document.querySelector(col_id) == null) {
                break;
            }
            last_col_id = col_id;
        }
        if (last_col_id == '') {
            last_col_id = '#id_event_rule_params_set-0-param_id';
        }
        const param_id_obj = document.querySelector(last_col_id);
        if (typeof param_id_obj == 'undefined' || param_id_obj == null) {
            console.error('Param Id Object cannot be obtained.');
            return;
        }

        if (typeof event_iot_map_id == 'undefined' || event_iot_map_id == null || event_iot_map_id == '') {
            console.error('Event_Type_IOT_Type_Map id cannot be obtained.');
            param_id_obj.innerHTML = '';
            return;
        }
        const param_id = param_id_obj.value;
        if (typeof param_id == 'undefined' || param_id == null || param_id == '') {
            var inputURL = window.location.protocol + "//" + window.location.host + '/eventmanagement/ajax/get_paramid_by_event_type_iot_type_map_id/';
            $.ajax({
                url: inputURL,
                type: 'GET',
                data: { 'event_type_iot_type_map_id': event_iot_map_id },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                success: function (paramIdsByEventIOTMapId) {
                    if (paramIdsByEventIOTMapId != null && paramIdsByEventIOTMapId != '') {
                        param_id_obj.innerHTML = '';
                        for (var i = 0; i < paramIdsByEventIOTMapId.length; i++) {
                            var optionElement = document.createElement('option');
                            optionElement.value = paramIdsByEventIOTMapId[i].param_id;;
                            optionElement.text = paramIdsByEventIOTMapId[i].param_name;
                            param_id_obj.appendChild(optionElement);
                        }
                    }
                },
                error: function (error) {
                    console.error('Error fetching param ids by event_iot_map_ids:', error);
                }
            });
        }
    }

    function populateParmUnits() {
        var all_param_ids = ''
        for (var i = 0; true; i++) {
            var col_id = '#id_event_rule_params_set-' + i + '-param_id';
            var param_id_obj = document.querySelector(col_id);
            if (param_id_obj == null) {
                break;
            }
            all_param_ids += ',' + param_id_obj.value;
        }
        if (all_param_ids != '') {
            if (all_param_ids.startsWith(',')) {
                all_param_ids = all_param_ids.substring(1);
            }
            var inputURL = window.location.protocol + "//" + window.location.host + '/eventmanagement/ajax/get_param_unit_by_multiple_param_ids/';
            $.ajax({
                url: inputURL,
                type: 'GET',
                data: { 'param_ids': all_param_ids },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                success: function (data) {
                    var map = {};
                    for (var i = 0; i < data.length; i++) {
                        var param_id = data[i][0];
                        var unit_name = data[i][1];
                        map[param_id] = unit_name;
                    }
                    for (var i = 0; true; i++) {
                        var param_id_obj = document.querySelector('#id_event_rule_params_set-' + i + '-param_id');
                        var value1_obj = document.querySelector('#id_event_rule_params_set-' + i + '-value1');
                        var value1_unit_obj = document.querySelector('#id_event_rule_params_set-' + i + '-value1_unit');
                        var value2_obj = document.querySelector('#id_event_rule_params_set-' + i + '-value2');
                        var value2_unit_obj = document.querySelector('#id_event_rule_params_set-' + i + '-value2_unit');
                        if (param_id_obj == null) {
                            break;
                        }
                        if (value1_obj.value != '') {
                            value1_unit_obj.value = map[param_id_obj.value];
                        }
                        if (value2_obj.value != '') {
                            value2_unit_obj.value = map[param_id_obj.value];
                        }
                    }
                },
                error: function (error) {
                    console.error('Error fetching Unit by Param Id:', error);
                }
            });
        }
    }

    function populateParamDropDownForEditableField() {
        var enabled_paramids_cols = ''
        for (var i = 0; true; i++) {
            var col_id = '#id_event_rule_params_set-' + i + '-param_id';
            var param_id_obj = document.querySelector(col_id);
            if (param_id_obj == null) {
                break;
            }
            if (!param_id_obj.disabled) {
                enabled_paramids_cols += ',' + col_id;
            }
        }
        if (enabled_paramids_cols != '') {
            if (enabled_paramids_cols.startsWith(',')) {
                enabled_paramids_cols = enabled_paramids_cols.substring(1);
            }
            var enabled_paramids_cols_arr = enabled_paramids_cols.split(',');
            const event_iot_map_id_obj = document.querySelector('#id_event_iot_map_id');
            if (typeof event_iot_map_id_obj == 'undefined' || event_iot_map_id_obj == null) {
                console.error('Event_Type_IOT_Type_Map  Object cannot be obtained.');
                return;
            }
            const event_iot_map_id = event_iot_map_id_obj.value;
            if (typeof event_iot_map_id == 'undefined' || event_iot_map_id == null || event_iot_map_id == '') {
                console.error('Event_Type_IOT_Type_Map id cannot be obtained.');
                return;
            }
            var inputURL = window.location.protocol + "//" + window.location.host + '/eventmanagement/ajax/get_paramid_by_event_type_iot_type_map_id/';
            $.ajax({
                url: inputURL,
                type: 'GET',
                data: { 'event_type_iot_type_map_id': event_iot_map_id },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                success: function (paramIdsByEventIOTMapId) {
                    if (paramIdsByEventIOTMapId != null && paramIdsByEventIOTMapId != '') {
                        for (var col_index = 0; col_index < enabled_paramids_cols_arr.length; col_index++) {
                            var temp_param_id_obj = document.querySelector(enabled_paramids_cols_arr[col_index]);
                            temp_param_id_obj.innerHTML = '';
                            for (var i = 0; i < paramIdsByEventIOTMapId.length; i++) {
                                var optionElement = document.createElement('option');
                                optionElement.value = paramIdsByEventIOTMapId[i].param_id;;
                                optionElement.text = paramIdsByEventIOTMapId[i].param_name;
                                temp_param_id_obj.appendChild(optionElement);
                            }
                        }
                    }
                },
                error: function (error) {
                    console.error('Error fetching param ids by event_iot_map_ids:', error);
                }
            });
        }
    }

    $(document).ready(function () {
        const $carousel = $('#content-main form #jazzy-carousel');
        const $tabs = $('#content-main form #jazzy-tabs');
        const $collapsible = $('#content-main form #jazzy-collapsible');

        // Ensure all raw_id_fields have the search icon in them
        $('.related-lookup').append('<i class="fa fa-search"></i>');

        // Style the inline fieldset button
        $('.inline-related fieldset.module .add-row a').addClass('btn btn-sm btn-default float-right');
        $('div.add-row>a').addClass('btn btn-sm btn-default float-right');

        // Ensure we preserve the tab the user was on using the url hash, even on page reload
        if ($tabs.length) { handleTabs($tabs); }
        else if ($carousel.length) { handleCarousel($carousel); }
        else if ($collapsible.length) { handleCollapsible($collapsible); }

        applySelect2();

        $('body').on('change', '.related-widget-wrapper select', function (e) {
            const event = $.Event('django:update-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented() && typeof (window.updateRelatedObjectLinks) !== 'undefined') {
                updateRelatedObjectLinks(this);
            }
        });
        populateParmUnits();
        populateParamDropDownForEditableField();
    });

    // Apply select2 to all select boxes when new inline row is created
    django.jQuery(document).on('formset:added', applySelect2);

})(jQuery);
