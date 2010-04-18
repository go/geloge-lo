function getUserGelo(url){
    geloDataGroup.closeAllInfoWindow();
    geloDataGroup.eraseLine();
    geloDataGroup.removeAll();
    $("#timeline").empty();
    
    var account = $("#account").val();
    $.blockUI({message: "Loading Information for " + account});
    $.getJSON( url, "", buildGeroFromJSON);
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
                      
                      var account = $.query.get('account');
                      if(account){
                          $("#account").val(account);    
                          getUserGelo("/get_user_gelo.json?account=" + account);
                      }
                      


                  });
