
// Get user data from Python server
//
$.getJSON( "/users", { rand: Date.now() }, function( data ) {

    var hasUser = false;

    Object.keys(data).forEach(function(userMac) {

        // If connected, append name
        //
        if(data[userMac].connected){
	    hasUser = true;
            $('body').append('<p>' + data[userMac].name + '</p>');
        }
    })

    if (!hasUser) {
        $('body').append('<p class="nametag">No users were found.</p>');
    }
});
