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
    
    // Dynamically lay out the chat page (NOT YET; STILL BUGGY)
    // fixlayout();
    // window.scroll(0, 100000);
});

function fixlayout() {
    // Get references to the elements we'll be rearranging
    var chat = $('#chat');
    var header = $('#header');
    var sidebar = $('#users');
    var post = $('#post');
    var footer = $('#footer');

    // Store the margins needed for the chat box before these
    // the elements on which they're based change positions
    var chatTop = chat.position().top;
    var chatBottom = post.position().top;
    
    // Affix header and users sidebar in place
    affix(sidebar, sidebar.position());
    affix(header, header.position());
    
    // Affix footer to the bottom
    affix(footer, { bottom: 0, left: footer.position().left });
    
    // Affix the post box on top of the footer
    affix(post, { bottom: footer.outerHeight(), left: post.position().left });
    
    // Adjust the margins of the chat box to compensate for the
    // sizes of the now-fixed surrounding elements
    chat.css({
        marginTop: chatTop + 'px',
        marginBottom: 1 + footer.outerHeight() + post.outerHeight() + 'px',
    });
    
    // Make the sidebar fill its space vertically
    var sidebarHeight = window.innerHeight - header.outerHeight() - footer.outerHeight() - 4;
    sidebar.css('height', sidebarHeight + 'px');
}

function affix(el, pos) {
    var cssRule = { position: 'fixed' };
    for (attr in pos) {
        cssRule[attr] = pos[attr] + 'px';
    }
    el.css(cssRule);
}