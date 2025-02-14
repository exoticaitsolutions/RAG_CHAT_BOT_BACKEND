jQuery(document).ready(function(){
    console.log('helllo from the jquery............');
    var $sidebar = $('nav');
    $('.toggle').on('click', function () {
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