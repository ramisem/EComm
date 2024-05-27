var org_model_name = '';

function populateModelNameByAppName() {
    const id_model_app_name_obj = document.querySelector('#id_model_app_name');
    const id_model_name_obj = document.querySelector('#id_model_name');
    if (typeof id_model_app_name_obj == 'undefined' || id_model_app_name_obj == null) {
        console.error('App name Object cannot be obtained.');
        return;
    }
    if (typeof id_model_name_obj == 'undefined' || id_model_name_obj == null) {
        console.error('Model name Object cannot be obtained.');
        return;
    }
    const org_value = id_model_name_obj.value;
    org_model_name = org_value;
    id_model_name_obj.innerHTML = '';
    const option = document.createElement('option');
    option.value = '';
    option.text = 'Select an option';
    id_model_name_obj.appendChild(option);
    if ('' == id_model_app_name_obj.value) {
        return;
    }
    inputURL = window.location.protocol + "//" + window.location.host + '/dashboard/ajax/get_model_names/';
    $.ajax({
        url: inputURL,
        type: 'GET',
        data: { 'app_name': id_model_app_name_obj.value },
        dataType: 'json',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        success: function (response) {
            if (response.model_data) {
                response.model_data.forEach(function (model) {
                    const option = document.createElement('option');
                    option.value = model.model_name;
                    option.text = model.verbose_name;
                    id_model_name_obj.appendChild(option);
                });
            } else if (response.error) {
                alert(response.error);
            }
            id_model_name_obj.value = org_value;
        },
        error: function (error) {
            console.error('Error fetching Model info based on App name:', error);
        }
    });
}

function populateDateOperationFieldNameByAppName() {
    const id_model_app_name_obj = document.querySelector('#id_model_app_name');
    const id_model_name_obj = document.querySelector('#id_model_name');
    const id_date_field_name_obj = document.querySelector('#id_date_field_name');
    const id_operation_field_name_obj = document.querySelector('#id_operation_field_name');
    if (typeof id_model_app_name_obj == 'undefined' || id_model_app_name_obj == null) {
        console.error('App name Object cannot be obtained.');
        return;
    }
    if (typeof id_model_name_obj == 'undefined' || id_model_name_obj == null) {
        console.error('Model name Object cannot be obtained.');
        return;
    }
    if (typeof id_date_field_name_obj == 'undefined' || id_date_field_name_obj == null) {
        console.error('Date-field Object cannot be obtained.');
        return;
    }
    if (typeof id_operation_field_name_obj == 'undefined' || id_operation_field_name_obj == null) {
        console.error('Operation-field Object cannot be obtained.');
        return;
    }
    const org_date_field_name = id_date_field_name_obj.value;
    id_date_field_name_obj.innerHTML = '';
    const option = document.createElement('option');
    option.value = '';
    option.text = 'Select an option';
    id_date_field_name_obj.appendChild(option);
    const org_operation_field_name = id_operation_field_name_obj.value;
    id_operation_field_name_obj.innerHTML = '';
    const option1 = document.createElement('option');
    option1.value = '';
    option1.text = 'Select an option';
    id_operation_field_name_obj.appendChild(option1);
    var model_name = '';
    if (id_model_name_obj.value != '') {
        model_name = id_model_name_obj.value;
    }
    else {
        model_name = org_model_name
    }
    if ('' == model_name || '' == id_model_app_name_obj.value) {
        return;
    }
    inputURL = window.location.protocol + "//" + window.location.host + '/dashboard/ajax/get_date_and_operation_field_names/';
    $.ajax({
        url: inputURL,
        type: 'GET',
        data: { 'app_name': id_model_app_name_obj.value, 'model_name': model_name },
        dataType: 'json',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        success: function (response) {
            if (response.datetime_fields) {
                response.datetime_fields.forEach(function (datetime_field) {
                    const option = document.createElement('option');
                    option.value = datetime_field.field_name;
                    option.text = datetime_field.verbose_name;
                    id_date_field_name_obj.appendChild(option);
                });
            } else if (response.error) {
                alert(response.error);
            }
            id_date_field_name_obj.value = org_date_field_name;
            if (response.operation_fields) {
                response.operation_fields.forEach(function (operation_field) {
                    const option1 = document.createElement('option');
                    option1.value = operation_field.field_name;
                    option1.text = operation_field.verbose_name;
                    id_operation_field_name_obj.appendChild(option1);
                });
            } else if (response.error) {
                alert(response.error);
            }
            id_operation_field_name_obj.value = org_operation_field_name;
        },
        error: function (error) {
            console.error('Error fetching field info based on Model name:', error);
        }
    });
}

$(document).ready(function () {
    populateModelNameByAppName();
    populateDateOperationFieldNameByAppName();
});