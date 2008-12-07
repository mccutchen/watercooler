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
        if (!/^\w+$/.test(userName))
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
});
