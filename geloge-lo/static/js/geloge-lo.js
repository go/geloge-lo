var geloDataGroup;
var map;
var zoom;
var date = new Date();
var selected = 0;
var debug_enable = false;

var tweet_color = 'rgb(150, 150, 150)';
var tweet_color_giotagged = 'rgb(0, 0, 0)';
var tweet_color_selected = 'rgb(255, 0, 0)';

function stringToDate(datestr){
    var datetime = datestr.split(' ');
    var date = datetime[0].split('-');
    var time = datetime[1].split(':');
    debug(time);
    return new Date(parseInt(date[0]),
                    parseInt(date[1]-1),
                    parseInt(date[2]), 
                    parseInt(time[0]),
                    parseInt(time[1]),
                    parseInt(time[2]));
}
var GeloElementFromJSON = function(datestr, text, gelo){
    var ret = new Object();
        
    ret.date = stringToDate(datestr);
    ret.date.setHours(ret.date.getHours() - ret.date.getTimezoneOffset()/60);

    ret.text = text;
    ret.gelo = gelo;

    ret.datestr = function(){
        return this.date.toString();  
    };
    return ret;
};

var GeloData = function(marker,  htmlElement){
    var ret = new Object();
    ret.isSelected = false;
    ret.marker = marker;
    ret.htmlElement = htmlElement;
    ret.select = function(animation){
        var marker = this.marker;
        if(marker){
            marker.infoWindow.open(map, marker);
            $(this.htmlElement).css('color', tweet_color_selected);
        }
        var top = $(this.htmlElement).offset().top - 50;
        if(animation){
            $('html,body').animate({ scrollTop: top }, 'slow');            
        }else{
            $('html,body').scrollTop(top);
        }
        
        this.isSelected = true;
    };

    ret.unselect = function(){
        this.marker.infoWindow.close();
        $(this.htmlElement).css('color', tweet_color_giotagged);
        this.isSelected = false;
    };

    return ret;
};

var GeloDataGroup = function(){
    var ret = new Object();
    ret.geloDataList = [];

    ret.push = function(geloData){
        geloData.parent = this;
        this.geloDataList.push(geloData);
    };

    ret.getGeloDataByMarker = function(marker){
        for(var i in this.geloDataList){
            if(this.geloDataList[i].marker == marker){
                return this.geloDataList[i];
            }
        }
        return null;
    };

    ret.getGeloDataByHtmlElement = function(htmlElement){
        for(var i in this.geloDataList){
            if(this.geloDataList[i].htmlElement == htmlElement){
                return this.geloDataList[i];
            }
        }
        return null;
    };

    ret.getHtmlElementByMarker = function(marker){
        for(var i in this.geloDataList){
            if(this.geloDataList[i].marker == marker){
                return this.geloDataList[i].htmlElement;
            }
        }
        return null;
    };

    ret.getMarkerByHtmlElement = function(htmlElement){
        for(var i in this.geloDataList){
            if(this.geloDataList[i].htmlElement == htmlElement){
                return this.geloDataList[i].marker;
            }
        }
        return null;
    };

    ret.eachGeloData = function(func){
        for(var i in this.geloDataList){
            func(this.geloDataList[i]);
        }
    };

    ret.closeAllInfoWindow = function(){
        var closeAllWindowFunc = function(gd){
            gd.marker.infoWindow.close();
        };
        this.eachGeloData(closeAllWindowFunc);
    };

    ret.removeAll = function(){
        this.closeAllInfoWindow();
        this.eraseLine();
        var removeAllMarkerFromMap = function(gd){
            gd.marker.setMap(null);
        };
        this.eachGeloData(removeAllMarkerFromMap);
        this.geloDataList = [];

    };

    ret.cssForAllHtmlElements = function(key, val){
        var setCSSFunc = function(gd){
            $(gd.htmlElement).css(key, val);
        };
        this.eachGeloData(setCSSFunc);
    };

    ret.drawLine = function(){
        var coordinates = [];
        for(var i in this.geloDataList){
            coordinates.push(this.geloDataList[i].marker.position);
        }
        
        if(this.path){
            this.path.setMap(null);
        }
        this.path = new google.maps.Polyline({
                                                 path: coordinates, 
                                                 strokeColor: "#0000FF",
                                                 strokeOpacity: 0.5,
                                                 strokeWeight: 2
                                             });
        this.path.setMap(map);
    };

    ret.eraseLine = function(){
        if(this.path){
            this.path.setMap(null);            
        }

    };

    ret.getCurrentSelected = function(){
        var index = this.getCurrentSelectedIndex();
        if(index != null){
            return this.geloDataList[index];
        }
        return null;
    };

    ret.getCurrentSelectedIndex = function(){
        for(var i  = 0; i < this.geloDataList.length; i++){
            if(this.geloDataList[i].isSelected){
                return i;
            }
        }
        return null;
    };

    ret.getSlicedGeloList = function(start, end){
        return geloDataGroup.geloDataList.slice(start, end)
    };

    ret.select = function(geloData, animation){
        var current = this.getCurrentSelected();
        if(current){
            current.unselect();
        }
        geloData.select(animation);
    };

    ret.selectRelative = function(diff){
        var index = this.getCurrentSelectedIndex();
        if(index  == null){
            this.geloDataList[0].select();
            return true;
        }
        if(!this.geloDataList[index+diff]){
            return false;
        }
        this.geloDataList[index].unselect();        
        this.geloDataList[index+diff].select();        
        return true;
    };

    ret.selectNext = function(){
        return this.selectRelative(-1);
    };

    ret.selectPrev = function(){
        return this.selectRelative(1);
    };

    return ret;
};

function debug(val){
    if(!debug_enable){
        return;
    }

    var elem = document.getElementById("debug");
    if(elem){
        elem.innerHTML = val;        
    }
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

function setPosition(geloDataList){
    debug(geloDataList[0].marker.position);
    var lat_max = geloDataList[0].marker.position.lat();
    var lat_min = geloDataList[0].marker.position.lat();
    var lng_max = geloDataList[0].marker.position.lng();
    var lng_min = geloDataList[0].marker.position.lng();
    
    for(var i = 1; i < geloDataList.length; i++){
        var lat = geloDataList[i].marker.position.lat();
        var lng = geloDataList[i].marker.position.lng();
        
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
        zoom: 2,
        center: new google.maps.LatLng(0, 0), 
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
}

function createMarker(gelodata){
    var marker = new google.maps.Marker({
                                            position: new google.maps.LatLng(gelodata.gelo[0], 
                                                                             gelodata.gelo[1]), 
                                            map: map, 
                                            title: 'Geloge-Lo'
                                        });
    marker.infoWindow = new google.maps.InfoWindow({
                                                       content: '<div style="height:200px;">' +
                                                           gelodata.datestr() + 
                                                           "<br />" + 
                                                           gelodata.text + 
                                                           "</div>"
                                                   });
    return marker;
}

function addGeloMarker(geloDataGroup, geloelem){
    var tweet = document.createElement("div");
    $(tweet).addClass('tweet');
    $(tweet).css('color', tweet_color);
    var marker = null;
    if(geloelem.gelo){ // if geolocation foun
        $(tweet).css('color', tweet_color_giotagged);
        marker = createMarker(geloelem);
        var geloData = new GeloData(marker, tweet);
        marker.geloParent = geloDataGroup;
        geloDataGroup.push(geloData);
        google.maps.event.addListener(marker, 'click', function() {
                                          var geloData = marker.geloParent.getGeloDataByMarker(marker);
                                          marker.geloParent.select(geloData, true);
                                      });
    }
    tweet.geloParent = geloDataGroup;
    tweet.onclick = function(mouseEvent){
        var geloData = this.geloParent.getGeloDataByHtmlElement(this);
        this.geloParent.select(geloData, true);
    };

    tweet.innerHTML = 
        '<span>' + geloelem.text + '</span>' +
        '<br />' +
        '</span><span style="font-size: 70%; margin-left: 40%;">' + geloelem.datestr() + '</span>';
    if(marker){
        $(tweet).css('cursor', 'hand');
    }
    $("#timeline").append($(tweet));
    //$("#timeline").append($(document.createElement('hr')));
}

function buildGeroFromJSON(result){
    for(i in result){
        var geloelem = new GeloElementFromJSON(result[i][0], result[i][1], result[i][2]);
        addGeloMarker(geloDataGroup, geloelem);
    }

    geloDataGroup.drawLine();
    setPosition(geloDataGroup.geloDataList);
    $.unblockUI();
}    


function event_up(){
    geloDataGroup.selectNext();
}

function event_down(){
    geloDataGroup.selectPrev();
}


debug("ok");

