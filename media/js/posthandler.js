var PostHandler = (function() {
    var timestamps = [];
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
        var cls = 'ts' + timestamp + ((username == UserHandler.user()) ? ' me': '');
        var src = '<tr class="' + cls + '"><th>' + username + '</th><td>' + content + '</td></tr>'
        $('#chat').append(src);
        // Always scroll to the bottom (ugly hack, necessary right now)
        window.scroll(0, 100000);
    }
    
    function pingCallback(data) {
        data.posts.each(function(post) {
            if (!timestamps.contains(post.timestamp)) {
                timestamps.push(post.timestamp);
                addPost(post.timestamp, post.user, post.content);
            }
        });
        UserHandler.update(data.active_users, data.inactive_users);
    }
    
    function init() {
        posturl = $('#post-form').attr('action');
        pingurl = $('#post-pingurl').val();
        
        // Get a list of timestamps of the posts already on the page
        $('#chat tr').each(function(i) {
            var ts = gettimestamp($(this).attr('class'));
            timestamps.push(ts);
        });
        
        window.setInterval(function() {
            var latest = timestamps[timestamps.length - 1] || 0;
            data = {'latest': latest}
            $.post(pingurl, data, pingCallback, 'json');
        }, PINGINTERVAL);
        
        // Wire up event listeners.
        $('#post-form').submit(function(event) {
            // Only submit the post if it is not blank.
            var content = this['content'].value;
            if (!content.isEmpty()) {
                $.post(posturl, { 'content': content, }, function(data) {
                    timestamps.push(data.timestamp);
                    addPost(data.timestamp, UserHandler.user(), data.content);
                }, 'json');
                
                // Remove the "empty" row from the DOM, if it exists
                $('#chat tr.empty').remove();
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
        
        // This is a bad solution, but it'll have to do for now
        window.scroll(0, 100000);
    }
    
    return {
        init: init,
    };
})();