// Client-side form validation for the registration page
$(function() {
    // Before the registration form is submitted, ensure that the
    // passwords match.
    $('#register').submit(function(event) {
        var a = $('#id_password1').val();
        var b = $('#id_password2').val();
        
        // If the passwords don't match, report the error and
        // cancel the form submission.
        if (a != b) {
            var error = '<p class="error">Passwords do not match.</p>';
            $(this).before(error);
            return false;
        }
        
        // Otherwise, allow the form submission to continue.
        return true;
    });
});