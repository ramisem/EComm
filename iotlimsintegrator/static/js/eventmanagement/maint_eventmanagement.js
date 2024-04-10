function populateIOTTypeByEventType() {
    const id_event_type_id_obj = document.querySelector('#id_event_type_id');
    const id_iot_type_id_obj = document.querySelector('#id_iot_type_id');
    var id_event_type_id = id_event_type_id_obj.value;
    var id_iot_type_id = id_iot_type_id_obj.value;
    if (typeof id_event_type_id_obj == 'undefined' || id_event_type_id_obj == null) {
        console.error('Event type Object cannot be obtained.');
        return;
    }
    if (typeof id_iot_type_id_obj == 'undefined' || id_iot_type_id_obj == null) {
        console.error('IOT type Object cannot be obtained.');
        return;
    }
    var inputURL = '';
    if (typeof id_event_type_id == 'undefined' || id_event_type_id == null || id_event_type_id == '') {
        console.error('Event type id cannot be obtained.');
        return;
    }
    inputURL = window.location.protocol + "//" + window.location.host + '/eventmanagement/ajax/get_iot_types_by_event_type/';
    $.ajax({
        url: inputURL,
        type: 'GET',
        data: { 'event_type_id': id_event_type_id },
        dataType: 'json',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        success: function (data) {
            id_iot_type_id_obj.innerHTML = '';
            for (var i = 0; i < data.length; i++) {
                var optionElement = document.createElement('option');
                optionElement.value = data[i].iot_type_id;
                optionElement.text = data[i].model_name;
                id_iot_type_id_obj.appendChild(optionElement);
            }
            if (id_iot_type_id && Array.from(id_iot_type_id_obj.options).some(option => option.value === id_iot_type_id)) {
                id_iot_type_id_obj.value = id_iot_type_id;
            }
        },
        error: function (error) {
            console.error('Error fetching IOT Type based on Event Type:', error);
        }
    });
}

function populateParamUnit(id) {
    const value_obj = document.querySelector('#' + id);
    const value_unit_obj = document.querySelector('#' + id + '_unit');
    if (typeof value_obj == 'undefined' || value_obj == null) {
        console.error('Value Object cannot be obtained.');
        return;
    }
    if (typeof value_unit_obj == 'undefined' || value_unit_obj == null) {
        console.error('Value1 Unit Object cannot be obtained.');
        return;
    }
    var value = value_obj.value;
    if (typeof value == 'undefined' || value == null || value == '') {
        value_unit_obj.value = '';
        console.log('Value cannot be obtained.');
        return;
    }
    const delimiter = '-';
    const parts = id.split(delimiter);

    if (parts.length >= 2) {
        const extractedString = parts.slice(0, 2).join(delimiter);
        var param_id_obj = document.querySelector('#' + extractedString + '-param_id');
        if (typeof param_id_obj == 'undefined' || param_id_obj == null) {
            console.error('Param Id Object cannot be obtained.');
            return;
        }
        var param_id = param_id_obj.value;
        if (typeof param_id == 'undefined' || param_id == null || param_id == '') {
            value_unit_obj.value = '';
            console.log('Param Id cannot be obtained.');
            return;
        }
        var inputURL = window.location.protocol + "//" + window.location.host + '/eventmanagement/ajax/get_param_unit_by_param_id/';
        $.ajax({
            url: inputURL,
            type: 'GET',
            data: { 'param_id': param_id },
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function (unit) {
                value_unit_obj.value = unit;
            },
            error: function (error) {
                console.error('Error fetching Unit by Param Id:', error);
            }
        });

    } else {
        console.log('Delimiter not found in the string.');
    }

}
