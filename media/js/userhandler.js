var UserHandler = (function() {
    // The current user's username
    var user;
    var usersObj;
    
    function update(active, inactive) {
        // First, clear the current list of users
        usersObj.children('li').remove();
        
        // Then re-add the active and inactive users
        active.each(function(u) {
            var src = '<li class="active' + ((u == user) ? ' me':'') + '">' + u + '</li>';
            usersObj.append(src);
        });
        inactive.each(function(u) {
            var src = '<li class="inactive">' + u + '</li>';
            usersObj.append(src);
        });
    }
    
    function init() {
        // Figure out what username we're posting under
        user = $('#post-username').val();
        
        // Get a reference to the users <ul> element
        usersObj = $('#users ul').eq(0);
    }
    
    return {
        init: init,
        update: update,
        me: user,
    };
})();
