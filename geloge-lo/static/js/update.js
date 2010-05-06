var marker = null;

function press_post(){
    var pos = marker.getPosition();
    var lat = (new Number(pos.lat())).toFixed(8);
    var lng = (new Number(pos.lng())).toFixed(8);
    var status = $('#status').val();
    var query = 
        '?status=' + status +
        '&lat=' + lat +
        '&lng=' + lng;
        
        
    $.ajax({
               type: "GET",
               url: "/api/update" + query,
               success: function(msg){
                   alert( "Data Saved");
               }
           });
}

function post_initialize(){
    initialize();
    var myLatLng = new google.maps.LatLng(0,0);
    marker = new google.maps.Marker({
                                        position: myLatLng, 
                                        map: map
                                    });
    marker.setDraggable(true);
}
