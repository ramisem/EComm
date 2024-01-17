const PAGE_SIZE = 5;
let currentPage = 1;

function loadCategories() {
    var inputURL = '';
    if(typeof logged_in_emailid != 'undefined' && logged_in_emailid != null)
        inputURL = window.location.protocol + "//" + window.location.host+'/partial_views/categories/?logged_in_emailid='+logged_in_emailid;
    else
        inputURL = window.location.protocol + "//" + window.location.host+'/partial_views/categories/';
    $.ajax({
        url: inputURL,
        type: 'GET',
        data: {'page': currentPage, 'page_size': PAGE_SIZE},
        headers: {
            'X-CSRFToken': getCSRFToken()  // Include the CSRF token in the headers
        },
        success: function (response) {
            // Append the fetched categories to the dropdown
            $('#categories-dropdown').append(response.categories_html);

            // Update the current page for the next request
            currentPage += 1;
        },
        error: function (error) {
            console.error('Error fetching categories:', error);
        }
    });
}

function toggleShowButton(){
    var obj_more_slide_open = document.querySelector('.more_slide_open');
    var obj_show_more_toggle_button = document.getElementById('show_more_toggle_button');
    if(obj_more_slide_open!=null && obj_show_more_toggle_button!=null){
        if(obj_more_slide_open.style.display == 'none'){
            obj_more_slide_open.style.display = 'block';
            obj_show_more_toggle_button.innerHTML = '<span class="less_icon"></span> <span class="heading-sm-1">Show less...</span>';
        }
        else{
            obj_more_slide_open.style.display = 'none';
            obj_show_more_toggle_button.innerHTML = '<span class="icon"></span> <span class="heading-sm-1">Show more...</span>';
        }
    }
}

document.querySelectorAll('.categories-button-active').forEach(function (button){
    button.addEventListener('click', function () {
       loadCategories();
    });
});
