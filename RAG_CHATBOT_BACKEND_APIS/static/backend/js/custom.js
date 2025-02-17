jQuery(document).ready(function(){
    console.log('helllo from the jquery............');
    let messages = [];
    jQuery(".django-message").each(function () {
        messages.push({ text: $(this).data("text"), type: $(this).data("type") });
    })
    if (messages.length > 0) {
        let messageText = messages.map(m => m.text).join("\n");

        Swal.fire({
            title: "📢 Notifications",
            text: messageText,
            icon: messages.some(m => m.type === 'error') ? 'error' :
                messages.some(m => m.type === 'success') ? 'success' :
                    messages.some(m => m.type === 'warning') ? 'warning' : 'info',
            confirmButtonText: "OK"
        });
    }

    var $sidebar = $('nav');
    jQuery('.toggle').on('click', function () {
        $sidebar.toggleClass('active');
    });
    // signup_process Vaidationa and Ajax 
    jQuery("#signup_process").validate({
        messages: {
            username: {
                required: "Please enter the username",
                maxlength: "Username must be a maximum of 50 characters"
            },
            email: {
                required: "Please enter your email address",
                email: "Please enter a valid email address"
            },
            password1: {
                required: "Please enter your password",
                minlength: "Password must be at least 8 characters long",
                maxlength: "Password must not exceed 20 characters",
                pattern: "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
            },
            password2: {
                required: "Please confirm your password",
                minlength: "Password must be at least 8 characters long",
                maxlength: "Password must not exceed 20 characters",
                pattern: "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character",
                equalTo: "Password and confirmation must match"
            }, agree_terms: {
                required: "You must agree to the terms and conditions"
            }
        },
        rules: {
            username: {
                required: true,
                maxlength: 50,
            },
            email: {
                required: true,
                email: true,  // Ensure a valid email format
            },
            password1: {
                required: true,
                minlength: 8,  // Minimum length for password
                maxlength: 20,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$/,  // Strong password regex
            },
            password2: {
                required: true,
                minlength: 8,  // Minimum length for password
                maxlength: 20, // Maximum length fo
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$/,  // Strong password regex
                equalTo: "#password1"  // Ensure password2 matches password1,
                
            }, agree_terms: {
                required: true  // This makes the checkbox required
            }
        },
        submitHandler: async function(_form, e) {
            e.preventDefault();
            jQuery(".theme_btn").attr("disabled", false);
            _form.submit(); // Allow normal form submission
        }
    });

    // loginin_Process  Vaidationa and Ajax 
    jQuery("#login_process").validate({
        messages: {
            username_or_address: {
                required: "Please enter the username and Email address",
                maxlength: "Username must be a maximum of 50 characters"
            },
            password1: {
                required: "Please enter your password",
                minlength: "Password must be at least 8 characters long",
                maxlength: "Password must not exceed 20 characters",
                pattern: "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
            }
        },
        rules: {
            username_or_address: {
                required: true,
                maxlength: 50,
            },
            email: {
                required: true,
                email: true,  // Ensure a valid email format
            },
            password1: {
                required: true,
                minlength: 8,  // Minimum length for password
                maxlength: 20,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$/,  // Strong password regex
            }
        },
        submitHandler: async function(_form, e) {
            e.preventDefault();
            jQuery(`.theme_btn`).attr("disabled", true);
            _form.submit(); // Allow normal form submission
        }
    });


  });

  $(document).on('click', '#chat_bot_modal_box', async function(event) {
    let url = $(this).data("url"); // Get the data-url attribute
    let fullUrl = window.location.origin + url; // Convert it to a full URL
    let ajax_value_list ={ user_id: $(this).data("login-user-id") , chat_type: $(this).data("model-type") ,chat_id : $(this).data("chat_id")}
    // console.log(ajax_value_list);
    const [resPose] = await Promise.all([Ajax_response(fullUrl, "POST", ajax_value_list, '')]);
    if (resPose.status === 'success') {
        $("#modal_content").html(resPose.html); // Load response into modal
        $("#modalCenter").modal("show"); // Open modal    
    }  
});
$(document).on('click', '#chat_bot_delete', async function(event) {
    const form = document.createElement("form");
    let url = $(this).data("url"); // Get the data-url attribute
    form.method = "POST";
    form.id = "chat_bot_modal_form";
    form.action =url; // Modify as needed
    const csrfToken = document.createElement("input");
    csrfToken.type = "hidden";
    csrfToken.name = "csrfmiddlewaretoken";
    csrfToken.value = csrfToken1; // Django's csrf token
    form.appendChild(csrfToken);
    const userIdInput = document.createElement("input");
    userIdInput.type = "hidden";
    userIdInput.name = "user_id";
    userIdInput.value = $(this).data("login-user-id");
    form.appendChild(userIdInput);
    const chatTypeInput = document.createElement("input");
    chatTypeInput.type = "hidden";
    chatTypeInput.name = "curd_type";
    chatTypeInput.value = $(this).data("model-type");
    form.appendChild(chatTypeInput);
    document.body.appendChild(form);
    const botIdInput = document.createElement("input");
    botIdInput.type = "hidden";
    botIdInput.name = "chat_id";
    botIdInput.value = $(this).data("chat_id"); // Dynamic bot ID from Django context
    form.appendChild(botIdInput);

    Swal.fire({
        title: "Do you want to delete the bot?",
        showDenyButton: false,
        showCancelButton: true,
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel"
    }).then(async (result) => {
        /* Check if the user confirmed the deletion */
        if (result.isConfirmed) {
            form.submit();
        }
    });
    
    

});
