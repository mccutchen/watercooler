// Client-side form validation for the registration page
$(function() {
    // Before the registration form is submitted, ensure that the
    // passwords match.
    $('#register').submit(function(event) {
        // Gather up the data we're validating
        var thisForm = $(this);
        var userName = $('#id_username').val();
        var p1 = $('#id_password1').val();
        var p2 = $('#id_password2').val();
        
        // Collect any validation errors
        var errors = [];

        // Make sure the username is valid
        if (!(/^\w+$/.test(userName)))
            errors.push('Username must contain only letters, numbers, or underscores.');

        // Make sure the passwords match
        if (p1 != p2)
            errors.push('Passwords do not match.');
        
        // If we got a validation error, display an error message to
        // the user and cancel form submission.
        if (errors.length > 0) {
            errors.each(function(e) {
                thisForm.before('<p class="error">' + e + '</p>');
            });
            return false;
        }

        // Otherwise, allow the form submission to continue.
        return true;
    });
    
    // As the user types in a username, check to see if it's available
    $('#id_username').keyup(function(event) {
        var field = $(this);
        var unavailableEl = field.parent().children('span.unavailable');
        var username = this.value;
        var url = 'usernameAvailable/' + username + '/';
        
        // Make the Ajax request and either show or hide the
        // "Unavailable" message depending on the response.
        $.get(url, null, function(data) {
            if (data == '0')
                unavailableEl.css('visibility', 'visible');
            else
                unavailableEl.css('visibility', 'hidden');
        });
    });
});
