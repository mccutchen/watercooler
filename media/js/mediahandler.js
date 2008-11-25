var MediaHandler = (function() {
    var handlers = [];
    var maxWidth;

    function makehandler(name, re, fn) {
        handlers.push({
            name: name,
            re: re,
            fn: fn
        });
    }

    var url_re = /((http:\/\/|www\.){1,2}(www\.)?[A-z0-9\-.]+\.([A-z]{2,4}\.?)+[^\s]*\w)/i;
    var img_re = /\.(jpg|jpeg|gif|png)(\?[^\s]+)?$/i;
    var youtube_re = /^http:\/\/www\.youtube\.com\/watch\?v=([A-z0-9]{11})/i;
    var audio_re = /\.(mp3|aac)(\?[^\s]+)?$/i;

    makehandler('image', img_re, function(url, match) {
        return '<a href="' + url + '"><img src="' + url + '" alt="" style="max-width:' + maxWidth + 'px" /></a>';
    });
    makehandler('youtube', youtube_re, function(url, match) {
        return '<embed src="http://www.youtube.com/v/' + match[1] + '" type="application/x-shockwave-flash" width="425" height="344" style="max-width:' + maxWidth + 'px" />';
    });
    makehandler('audio', audio_re, function(url, match) {
        var flashvars = 'file=' + url + '&amp;backcolor=222222&amp;frontcolor=FFFFFFF&amp;lightcolor=999999';
        return '<embed src="http://static.overloaded.org/mediaplayer/player.swf" type="application/x-shockwave-flash" flashvars="' + flashvars + '" height="20" width="75%" />';
    });

    // Set up a default handler that just turns the URL into a link
    handlers.default_handler = function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    };

    // If s is a URL (ie, matches url_re), make sure that s starts with
    // http://.  Otherwise, return null.
    function ensure_url(s) {
        if (!url_re.test(s))
            return null;
        // Isolate the URL, which may be surrounded by other text
        var url = s.match(url_re)[1];
        // Ensure that the URL begins with http://
        return /^https?:\/\//.test(url) ? url : 'http://' + url;
    }

    function handle(content) {
        var url = ensure_url(content);

        // If we aren't looking at a URL, don't do anything to content
        if (!url)
            return content;

        // Any transformation done by a media handler will be stored here.
        var result;

        // Try to find a handler that matches the URL we're working on
        for (var i = 0; i < handlers.length; i++) {
            var handler = handlers[i];
            if ((match = url.match(handler.re))) {
                result = handler.fn(url, match);
                // Wrap the result in a div with a caption containing
                // the matched URL
                var caption = handlers.default_handler(url);
                result = '<div class="media">' + result + '<p>' + caption + '</p></div>';
                break;
            }
        }

        // If no handler was found, use the default handler
        result = result || handlers.default_handler(url);

        // Replace the URL
        return content.replace(url_re, result);
    }

    function init() {
        // Determine the maximum width of embedded objects
        maxWidth = $('#chat td').eq(0).innerWidth() - 20;

        // Run each post through the MediaHandler to transform
        // any links into inline media objects
        $('#chat td').each(function(i) {
            var el = $(this);
            var content = el.text();
            var results = MediaHandler.handle(content);
            if (results != content)
                el.html(results);
        });
    }

    return {
        handle: handle,
        init: init
    };
})();
