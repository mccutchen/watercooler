var PostHandler = (function() {
    var timestamps = [];
    var username;

    function gettimestamp(s) {
        if (m = /ts(\d+)/.exec(s))
            return m[1];
        return null;
    }
    
    function init() {
        // Figure out what username we're posting under
        username = document.getElementById('post-username').value;
        
        // Get a list of timestamps of the posts already on the page
        $('#chat tr').each(function(i) {
            var ts = gettimestamp($(this).attr('class'));
            timestamps.push(ts);
        });
        
        // Wire up event listeners.
        $('#post-form').submit(function(event) {
            // Only submit the post if it is not blank.
            var blank = /^\s*$/;
            event.preventDefault();
            return !blank.test(this['content'].value);
        });
    
        $('#post-content').keypress(function(event) {
            // Submit the post automatically if the user presses
            // the enter key.
            if (event.which == 13) {
                event.preventDefault();
                return $('#post-form').submit();
            }
        });
    }
    
    return {
        init: init,
    };
})();