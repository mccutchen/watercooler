var UserHandler = (function() {
    // The current user's username
    var currentUser;
    var activeUsers;
    var inactiveUsers;

    function update(active, inactive) {
        // First, clear the current list of users
        $('#users ul').children('li').remove();
        
        function userLink(u) {
            return '<a href="filter/?user=' + u + '">' + u + '</a>';
        }

        // Then re-add the active and inactive users
        active.each(function(u) {
            var src = '<li class="' + ((u == currentUser) ? ' me':'') + '">' + userLink(u) + '</li>';
            activeUsers.append(src);
        });
        inactive.each(function(u) {
            var src = '<li>' + userLink(u) + '</li>';
            inactiveUsers.append(src);
        });

        // If there were no active or inactive users, add a 'None'
        // under that heading
        var nonesrc = '<li class="empty">None</li>';
        if (active.length == 0)
            activeUsers.append(nonesrc);
        if (inactive.length == 0)
            inactiveUsers.append(nonesrc);
    }

    // The currentUser variable cannot be seen outside of the closure
    // created for the UserHandler due to some aspect of JavaScript
    // scoping that escapes me, so it must be returned from a function
    // (which can be seen outside of the closure).
    function user() {
        return currentUser;
    }

    function init() {
        // Figure out what username we're posting under
        currentUser = $('#post-username').val();

        // Get references to the active and inactive users <ul>
        // elements
        activeUsers = $('#users ul.active').eq(0);
        inactiveUsers = $('#users ul.inactive').eq(0);
    }

    return {
        init: init,
        update: update,
        user: user
    };
})();

// Initialize this object
$(UserHandler.init);