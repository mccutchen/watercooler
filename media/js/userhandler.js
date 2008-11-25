var UserHandler = (function() {
    // The current user's username
    var currentUser;
    var usersObj;

    function update(active, inactive) {
        // First, clear the current list of users
        usersObj.children('li').remove();

        // Then re-add the active and inactive users
        active.each(function(u) {
            var src = '<li class="active' + ((u == currentUser) ? ' me':'') + '">' + u + '</li>';
            usersObj.append(src);
        });
        inactive.each(function(u) {
            var src = '<li class="inactive">' + u + '</li>';
            usersObj.append(src);
        });
    }

    function user() {
        return currentUser;
    }

    function init() {
        // Figure out what username we're posting under
        currentUser = $('#post-username').val();

        // Get a reference to the users <ul> element
        usersObj = $('#users ul').eq(0);
    }

    return {
        init: init,
        update: update,
        user: user
    };
})();
