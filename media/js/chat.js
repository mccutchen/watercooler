$(function() {
    $('#post-content').keypress(function(e) {
        if (e.which == 13 && !e.shiftKey) {
            document.forms['post-form'].submit();
            return false;
        }
    });
});