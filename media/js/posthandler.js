var PostHandler = (function() {
    var timestamps = [];
    var username;
    var posturl;

    function gettimestamp(s) {
        if (m = /ts(\d+)/.exec(s))
            return m[1];
        return null;
    }
    
    function addPost(content) {
        content = MediaHandler.handle(content);
        var timestamp = (new Date().getTime());
        var src = '<tr class="me ts' + timestamp + '"><th>' + username + '</th><td>' + content + '</td></tr>'
        $('#chat').append(src);
    }
    
    function init() {
        // Figure out what username we're posting under
        username = $('#post-username').val();
        posturl = $('#post-form').attr('action');
        
        // Get a list of timestamps of the posts already on the page
        $('#chat tr').each(function(i) {
            var ts = gettimestamp($(this).attr('class'));
            timestamps.push(ts);
        });
        
        // Wire up event listeners.
        $('#post-form').submit(function(event) {
            // Only submit the post if it is not blank.
            event.preventDefault();
            var content = this['content'].value;
            if (!content.isEmpty()) {
                /*
                    This is what the AJAX implementation will do, once
                    it's finished.  But for now, this is disabled, so
                    the form submits as normal.
                
                    // Hide the "empty" row, if it exists
                    $('#chat tr.empty').css('display', 'none');
                    // Clear the user's input from the form
                    this['content'].value = '';
                    // Add the post to the page
                    addPost(content);
                */
                return true;
            }
            return false;
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