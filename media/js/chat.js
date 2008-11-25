$(function() {
    UserHandler.init();
    MediaHandler.init();
    PostHandler.init();
    
    // Dynamically lay out the chat page (NOT YET; STILL BUGGY)
    // $(document.body).click(function() {
    //         fixlayout();
    //     });
    fixlayout();
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
    var chatTop = header.outerHeight() + 1;
    var chatBottom = post.position().top;
    
    // Affix header and users sidebar in place
    affix(sidebar, { top: chatTop, right: 0} );
    affix(header, header.position());
    
    // Affix footer to the bottom
    affix(footer, { bottom: 0, left: 0 });
    
    // Affix the post box on top of the footer
    affix(post, { bottom: footer.outerHeight(), left: 0 });
    // Adjust the width of the post box
    post.css('width', chat.outerWidth());
    
    // Adjust the margins of the chat box to compensate for the
    // sizes of the now-fixed surrounding elements
    chat.css({
        marginTop: chatTop + 'px',
        marginBottom: 1 + footer.outerHeight() + post.outerHeight() + 'px',
    });
    
    // Make sure the page header is higher in z order than the chat box
    header.css('z-index', 1000);
    
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
