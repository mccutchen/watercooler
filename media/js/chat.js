$(function() {
    $('#post-submit').css('display', 'none');
    $('#post-content').keypress(function(e) {
        if (e.which == 13 && !e.shiftKey) {
            document.forms['post'].submit();
            return false;
        }
    });
});