$(function() {
    // Only submit the post if it is not blank.
    $('#post-form').submit(function(event) {
        var blank = /^\s*$/;
        event.preventDefault();
        return !blank.test(this['content'].value);
    });
    
    // Submit the post automatically if the user presses
    // the enter key.
    $('#post-content').keypress(function(event) {
        if (event.which == 13 && !event.shiftKey) {
            event.preventDefault();
            return $('#post-form').submit();
        }
    });
});