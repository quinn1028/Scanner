
// Get user data from Python server
//
$.getJSON( "/users", function( data ) {
    Object.keys(data).forEach(function(userMac) {

        // If connected, append name
        //
        if(data[userMac].connected){
            $('body').append('<p>' + data[userMac].name + '</p>')
        }
    })
});
