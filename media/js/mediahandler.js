var MediaHandler = (function() {
    var handlers = [];
    
    function makehandler(name, re, fn) {
        handlers.push({
            name: name,
            re: re,
            fn: fn
        });
    }
    
    var url_re = /((http:\/\/|www\.){1,2}(www\.)?[A-z0-9\-.]+\.([A-z]{2,4}\.?)+[^\s]*\w)/i;
    var img_re = /\.(jpg|jpeg|gif|png)$/i;
    var youtube_re = /^http:\/\/www\.youtube\.com\/watch\?v=([A-z0-9]{11})/i;
    var audio_re = /\.(mp3|aac)$/i;
    
    makehandler('image', img_re, function(url, match) {
        return '<a href="' + url + '"><img src="' + url + '" alt="" /></a>';
    });
    makehandler('youtube', youtube_re, function(url, match) {
        return '<embed src="http://www.youtube.com/v/' + match[1] + '" type="application/x-shockwave-flash" width="300" height="200" />';
    });
    makehandler('audio', audio_re, function(url, match) {
        return '<embed src="http://static.overloaded.org/watercooler/mediaplayer/player.swf" type="application/x-shockwave-flash" flashvars="file=' + url + '&amp;backcolor=222222&amp;frontcolor=FFFFFFF&amp;lightcolor=999999" height="20" width="50%" />';
    });
    
    // Set up a default handler that just turns the URL into a link
    handlers.default = function(url) {
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
    
    var handle = function(content) {
        var url = ensure_url(content);
        
        // If we aren't looking at a URL, don't do anything to content
        if (!url)
            return content;
        
        // Any transformation done by a media handler will be stored here.
        var result;
        
        // Try to find a handler that matches the URL we're working on
        for (var i = 0; i < handlers.length; i++) {
            var handler = handlers[i];
            if (match = url.match(handler.re)) {
                result = handler.fn(url, match);
                break;
            }
        }
        
        // If no handler was found, use the default handler
        result = result || handlers.default(url);
        
        // Replace the URL
        return content.replace(url_re, result);
    }
    
    return { handle: handle };
})();