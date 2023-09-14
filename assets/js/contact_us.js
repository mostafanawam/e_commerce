$(document).ready(function() {



    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
            }
        }
    });



    function isValidEmail(email) {
        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return emailRegex.test(email);
    }


    function validate(name, subject, email, message) {
        if (name === "" || !/[a-zA-Z]/.test(name)) {
            return "Name field is required."
        }
        if (!isValidEmail(email)) {
            return "Please enter a valid email."
        }
        if (subject === "" || !/[a-zA-Z]/.test(subject)) {
            return "Subject field is required."
        }


        if (message === "") {
            return "Message field is required."

        }

        return ""
    }


    $('#btnSend').click(function(e) {
        e.preventDefault();

        var fullname = $("#name").val();
        var email = $("#email").val();
        var subject = $("#subject").val();
        var message = $("#message").val();


        var errors = validate(fullname, subject, email, message)
        if (errors === "") {
            $('#btnSend').html("Sending <i class='fa fa-spinner fa-spin'></i>")
            $('#btnSend').prop('disabled', true);

            $.ajax({
                type: 'POST',
                url: '/contact-us/',
                data: {
                    'fullname': fullname,
                    'email': email,
                    'subject': subject,
                    'message': message,
                },
                success: function(data) {
                    if (data.success == "success") {

                        $('#alert_errors').addClass('hidden')

                        $('#btnSend').html("Send")
                        $('#btnSend').prop('disabled', false);

                        $("#name").val("");
                        $("#email").val("");
                        $("#subject").val("");
                        $("#message").val("");

                    }


                }
            });

        } else {
            $('#alert_errors').removeClass('hidden')

            $('#alert_errors').html(errors)
        }


    });

});