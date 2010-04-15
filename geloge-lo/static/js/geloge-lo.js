var map;
var kinsityo;
var myhome;
var points = [];
var pointer = 0;
var zoom;
var date = new Date();
function debug(val){
    document.getElementById("debug").innerHTML = val;
}
n

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
    //var bound = getBounds(markers[0].position, markers[1].position);
    //map.fitBounds(bound);
    //pointer++;
    //if(pointer > points.length - 2){
    //pointer = 0;
    //}
    //map.setCenter(points[pointer]);
}

function initialize() {
    var myOptions = {
        zoom: 1,
        //center: points[0],
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);


        
    //map.setCenter(points[pointer]);
    map.setCenter(new google.maps.LatLng(35.656738,139.787636));
}

function start(){
    setPosition();
    
}
var markers = [];
function jsontest(){
    $.getJSON( "./ossan.json", "", function(result){
                   debug("hoge");
                   for(i in result){
                       var marker = new google.maps.Marker({
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
               });
}
debug("ok");