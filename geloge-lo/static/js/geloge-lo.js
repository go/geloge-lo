var markers = [];
var map;
var zoom;
var date = new Date();
function debug(val){
    document.getElementById("debug").innerHTML = val;
}

function getBounds(A, B){
    var ymax = A.lat() > B.lat() ? A.lat() : B.lat();
    var ymin = A.lat() <= B.lat() ? A.lat() : B.lat();
    var xmax = A.lng() > B.lng() ? A.lng() : B.lng();
    var xmin = A.lng() <= B.lng() ? A.lng() : B.lng();

    return new google.maps.LatLngBounds(
        new google.maps.LatLng(ymin, xmin), 
        new google.maps.LatLng(ymax, xmax)
    );
}

function setPosition(){
    var lat_max = markers[0].position.lat();
    var lat_min = markers[0].position.lat();
    var lng_max = markers[0].position.lng();
    var lng_min = markers[0].position.lng();

    for(var i = 1; i < markers.length; i++){
        var lat = markers[i].position.lat();
        var lng = markers[i].position.lng();
        
        if(lat_max < lat){ lat_max = lat; }
        if(lng_max < lng){ lng_max = lng; }
        if(lat_min > lat){ lat_min = lat; }
        if(lng_min > lng){ lng_min = lng; }
    }

    var bound = getBounds(new google.maps.LatLng(lat_min, lng_min),
                          new google.maps.LatLng(lat_max, lng_max));
    map.fitBounds(bound);
}

function initialize() {
    var myOptions = {
        zoom: 1,
        center: new google.maps.LatLng(0, 0), 
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
}


function jsontest(){
    var account = $("#account").val();
    $.getJSON( "/get_user_gelo.json?account=" + account, "", function(result){
                   for(i in result){
                       var tweet = document.createElement("div");
                       var marker = null;
                       if(result[i][2]){ // if geolocation found
                           marker = new google.maps.Marker({
                                                               position: new google.maps.LatLng(result[i][2][1], 
                                                                                                result[i][2][0]), 
                                                               map: map, 
                                                               title: i
                                                           });
                           marker.infoWindow = new google.maps.InfoWindow({
                                                                              content: '<div style="height:200px;">' + result[i][0] + "<br />" + result[i][1] + "</div>"
                                                                          });
                           
                           markers.push(marker);
                           google.maps.event.addListener(marker, 'click', function() {
                                                             for(i in markers){
                                                                 markers[i].infoWindow.close();   
                                                             }
                                                             this.infoWindow.open(map,this);
                                                         });
                       }

                       tweet.marker = marker;
                       tweet.onclick = function(){
                           for(i in markers){
                               markers[i].infoWindow.close();   
                           }
                           if(this.marker){
                               this.marker.infoWindow.open(map, this.marker);                               
                           }
                       };
                       
                       tweet.innerHTML = result[i][0] + "  " + result[i][1];
                       $("#timeline").append($(tweet));
                   }
                   setPosition();
               });
}
debug("ok");