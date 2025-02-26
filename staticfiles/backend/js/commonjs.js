let  ajaxResult = null;
const Ajax_response = async (url, method, values, beforetask, success, callback) => {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    jQuery.ajaxSetup({headers: {'X-CSRF-TOKEN': csrfToken}});
    return jQuery.ajax({
        type: method,
        url: url,
        data: values,
        beforeSend: function (msg) {
        },
        success: function (msg) {
            callback
        },
        error: function (_request, status, _error) {
        }
    });
};

function NotyfMessage(message, type) {
    var notyf = new Notyf();
    if (type === 'success') {
        notyf.success(message);
    } else if (type === 'error') {
        notyf.error(message);
    } else if (type === 'warning') {
        notyf.error(message);
    }
}