var PostHandler = (function() {
    var timestamps = [];
    var me;
    var posturl;
    var pingurl;
    
    var PINGINTERVAL = 3000;

    function gettimestamp(s) {
        if (m = /ts(\d+)/.exec(s))
            return parseInt(m[1], 10);
        return null;
    }
    
    function addPost(timestamp, username, content) {
        content = MediaHandler.handle(content);
        var cls = 'ts' + timestamp + ((username == me) ? ' me': '');
        var src = '<tr class="' + cls + '"><th>' + username + '</th><td>' + content + '</td></tr>'
        $('#chat').append(src);
    }
    
    function pingCallback(data) {
        data.posts.each(function(post) {
            if (!timestamps.contains(post.timestamp)) {
                timestamps.push(post.timestamp);
                addPost(post.timestamp, post.user, post.content);
            }
        });
    }
    
    function init() {
        // Figure out what username we're posting under
        me = $('#post-username').val();
        posturl = $('#post-form').attr('action');
        pingurl = $('#post-pingurl').val();
        
        // Get a list of timestamps of the posts already on the page
        $('#chat tr').each(function(i) {
            var ts = gettimestamp($(this).attr('class'));
            timestamps.push(ts);
        });
        
        window.setInterval(function() {
            data = {'latest': timestamps[timestamps.length - 1]}
            $.post(pingurl, data, pingCallback, 'json');
        }, PINGINTERVAL);
        
        // Wire up event listeners.
        $('#post-form').submit(function(event) {
            // Only submit the post if it is not blank.
            var content = this['content'].value;
            if (!content.isEmpty()) {
                $.post(posturl, { 'content': content, }, function(data) {
                    timestamps.push(data.timestamp);
                    addPost(data.timestamp, me, content);
                }, 'json');
                
                // Hide the "empty" row, if it exists
                $('#chat tr.empty').css('display', 'none');
                // Clear the user's input from the form
                this['content'].value = '';
            }
            event.preventDefault();
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