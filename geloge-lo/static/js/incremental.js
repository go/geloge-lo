var GeloBuffer = function(){
    var ret = new Object();
    ret.buff = [];

    ret.getOldest = function(){
        return this.buff.pop();
    };

    ret.getNewest = function(){
        return this.buff.shift();
    };

    ret.append = function(other){
        return this.buff = this.buff.concat(other);
    };

    ret.size = function(){
        return this.buff.length;
    };
    return ret;
};


var buffer_forward;
var buffer_backward;

function startUI(){
    buffer_forward = new GeloBuffer();
    buffer_backward = new GeloBuffer();


    if(geloDataGroup){
        geloDataGroup.removeAll();
        $("#timeline").empty();
    }

    var account = $("#account").val();
    if(!account){
        return;
    }

    $.blockUI({message: 'Loading Data for ' + account + '...'});
    // var url = "/get_user_gelo.json?account=" + account;
    var url = "/api/get_timeline";
    $.getJSON(url , "", function(result){
                  var ok = false;
                  buffer_backward.append(result);
                  while(!ok){
                      var newest = buffer_backward.getNewest();
                      if(newest == null){
                          break;
                      }

                      var geloelem = new GeloElementFromJSON(newest[0], newest[1], newest[2]);
                      addGeloMarker(geloDataGroup, geloelem);

                      if(newest[2]){
                          ok = true;
                      }
                  }

                  $.unblockUI();
              });
}

function event_up(){
    var success = geloDataGroup.selectNext();
    var index = geloDataGroup.getCurrentSelectedIndex();
    
    focus_near_by(index);
}

function event_down(){
    var success =  geloDataGroup.selectPrev();
    var index = geloDataGroup.getCurrentSelectedIndex();

    if(success){
        focus_near_by(index);
        return;
    }
    if(buffer_backward.size() > 0){
        var jsonElem = buffer_backward.getNewest();
        var geloelem = new GeloElementFromJSON(jsonElem[0], jsonElem[1], jsonElem[2]);
        addGeloMarker(geloDataGroup, geloelem);
        geloDataGroup.drawLine();
    }
    geloDataGroup.selectPrev();
    index = geloDataGroup.getCurrentSelectedIndex();
    focus_near_by(index);
    // setPosition(geloDataGroup.geloDataList);
}

function focus_near_by(index){
    if(index == 0){ 
        var focusDataList = geloDataGroup.getSlicedGeloList(0, index+2)
    }
    else{
        var focusDataList = geloDataGroup.getSlicedGeloList(index-1, index+2)
    }

    setPosition(focusDataList);
}

$(document).keypress(function(event) {
                         var up_key = 107; // k
                         var down_key = 106; //j
                         var pressed_key = event.which;
                         if(pressed_key == up_key){
                             debug("up");
                             event_up();
                         }
                         if(pressed_key == down_key){
                             debug("down");
                             event_down();
                         }
                     });

$(document).ready(function(){
                      geloDataGroup = GeloDataGroup();
                      if($.query.get('debug')){
                          debug_enable = true;
                      }
                      
                      //var account = $.query.get('account');
                      //if(account){
                      //$("#account").val(account);    
                      startUI();
                      //}
                      
                  });
