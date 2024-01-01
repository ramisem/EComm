function call_view_with_multiple_params(view_name,input_dict_obj){
    if(typeof view_name == 'undefined' || view_name == null){
        console.error('An error occurred: view_name cannot be obtained.');
        return;
    }
    if(typeof input_dict_obj != 'undefined' && input_dict_obj != null){
        $.ajax({
            url: view_name,
            method: 'POST',  // Use 'POST' if needed
            data: { 'data': JSON.stringify(input_dict_obj) },
            headers: {
                'X-CSRFToken': getCSRFToken()  // Include the CSRF token in the headers
            },
            success: function (response, status, xhr) {
                var contentType = xhr.getResponseHeader('Content-Type');
                if (contentType && contentType.indexOf('application/json') !== -1) {
                    console.log('Response is JSON:', response);
                } else if (contentType && contentType.indexOf('text/html') !== -1) {
                    console.log('Response is HTML:', response);
                } else {
                    console.log('Unexpected response type. Content-Type:', contentType);
                }
                console.log(response);
            },
            error: function (error) {
                if(typeof error != 'undefined' && error.responseText){
                    var errorString = error.responseText;
                    console.error('Below error occurred\n:', errorString);
                }
                else
                    console.error('Unexpected error occurred.');
            },
        });
    }
    else{
        console.error('An error occurred: input_dict_obj cannot be obtained.');
    }
}

//The below js assumes the obj to have the dictionary object in the below format
//input_dict_obj = {
//    {"package": "my_package", "method_name": "method1", "params": ("value1",)},
//    {"package": "my_package", "method_name": "method2", "params": ("value1", "value2")}
//}
function execute_command(input_dict_obj){
    call_view_with_multiple_params(window.location.protocol + "//" + window.location.host+'/utils/command/',input_dict_obj);
}

function getCSRFToken() {
    var name = 'csrftoken=';
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookieArray = decodedCookie.split(';');
    for (var i = 0; i < cookieArray.length; i++) {
        var cookie = cookieArray[i].trim();
        if (cookie.indexOf(name) == 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return null;
}

function logoff(autoredirect){
    if(typeof autoredirect != 'undefined' && autoredirect!=null && autoredirect==='Y'){
        window.location.href = window.location.protocol + "//" + window.location.host+'/user/sign-out/None'+'?autoredirect=' + encodeURIComponent('Y');
    }
    else
        window.location.href = window.location.protocol + "//" + window.location.host+'/user/sign-out/None';
}

function call_reset_session_timeout_command(){
    var props = [
        { package_name: 'utils.commands', method_name: 'reset_session_timeout', params: ['request'] },
    ];
    execute_command(props);
}
