jQuery(document).ready(function(){
    console.log('hello from the jQuery script...');

    let messages = [];
    jQuery(".django-message").each(function () {
        messages.push({ text: $(this).data("text"), type: $(this).data("type") });
    });

    if (messages.length > 0) {
        let messageText = messages.map(m => m.text).join("\n");
        Swal.fire({
            title: "📢 Notifications",
            
            text: messageText,
            icon: messages.some(m => m.type === 'error') ? 'error' :
                messages.some(m => m.type === 'success') ? 'success' :
                    messages.some(m => m.type === 'warning') ? 'warning' : 'info',
            confirmButtonText: "OK"
        }).then(() => {
            console.log("Notification displayed.");
        });
    }
    // Toggle sidebar
    var $sidebar = $('nav');
    jQuery('.toggle').on('click', function () {
        console.log('Toggling sidebar visibility');
        $sidebar.toggleClass('active');
    });

    // Signup Validation and Ajax
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
            },
            agree_terms: {
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
                email: true,
            },
            password1: {
                required: true,
                minlength: 8,
                maxlength: 20,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$/,
            },
            password2: {
                required: true,
                minlength: 8,
                maxlength: 20,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$/,
                equalTo: "#password1",
            },
            agree_terms: {
                required: true
            }
        },
        submitHandler: async function(_form, e) {
            e.preventDefault();
            console.log("Form submitted successfully.");
            jQuery(".theme_btn").attr("disabled", false);
            _form.submit();
        }
    });

    // Login Validation and Ajax
    jQuery("#login_process").validate({
        messages: {
            username_or_address: {
                required: "Please enter the username or email address",
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
                email: true,
            },
            password1: {
                required: true,
                minlength: 8,
                maxlength: 20,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$/,
            }
        },
        submitHandler: async function(_form, e) {
            e.preventDefault();
            console.log("Login form submitted.");
            jQuery(".theme_btn").attr("disabled", true);
            _form.submit();
        }
    });

    // Profile image upload preview
    var readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.profile-pic').attr('src', e.target.result);
                $(".file-upload").attr('value', e.target.result)
                console.log("Profile image loaded.");
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $(".file-upload").on('change', function(){
        console.log("File selected.");
        readURL(this);
    });

    $(".upload-button").on('click', function() {
        console.log("File upload button clicked.");
        $(".file-upload").click();
    });
});

// Chat Bot Modal Open
$(document).on('click', '#chat_bot_modal_box', async function(event) {
    let url = $(this).data("url");
    let fullUrl = window.location.origin + url;
    let ajax_value_list = {
        user_id: $(this).data("login-user-id"),
        chat_type: $(this).data("model-type"),
        chat_id: $(this).data("chat_id")
    };

    console.log("Opening chat bot modal with URL: ", fullUrl);
    const [resPose] = await Promise.all([Ajax_response(fullUrl, "POST", ajax_value_list, '')]);
    
    if (resPose.status === 'success') {
        $("#modal_content").html(resPose.html);
        $("#modalCenter").modal("show");
        console.log("Modal displayed with content.");
    }
});

// Chat Bot Delete Action
$(document).on('click', '#chat_bot_delete', async function(event) {
    const form = document.createElement("form");
    let url = $(this).data("url");
    form.method = "POST";
    form.id = "chat_bot_modal_form";
    form.action = url;

    const csrfToken = document.createElement("input");
    csrfToken.type = "hidden";
    csrfToken.name = "csrfmiddlewaretoken";
    csrfToken.value = csrfToken1; 
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
    botIdInput.value = $(this).data("chat_id");
    form.appendChild(botIdInput);

    Swal.fire({
        title: "Do you want to delete the bot?",
        showDenyButton: false,
        showCancelButton: true,
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel"
    }).then(async (result) => {
        if (result.isConfirmed) {
            console.log("Bot deletion confirmed.");
            form.submit();
        } else {
            console.log("Bot deletion canceled.");
        }
    });
});
