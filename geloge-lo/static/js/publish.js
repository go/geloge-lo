var account;
var oldest_tid = 0;
var is_processing = false;

function onError(xhr, status, error){
    alert("error");
    $.unblockUI();
    is_processing = false;
}

function onSuccess(obj){
    var last = obj[obj.length - 1];
    var tid = null;
    if(last){
        tid = last[last.length - 1];        
    }

    if(tid){
        oldest_tid = tid;
        buildGeroFromJSON(obj);
        var selected = geloDataGroup.getCurrentSelected();
        if(selected){
            selected.select(true);        
        }
    }else{
        $.unblockUI();        
    }
    is_processing = false;
    $("#append").css('display', 'inherit');
}
function getUserGelo(url){
    var account = $("#account").val();
    $.blockUI({message: "Loading Information for " + account});
    $.ajax({
               url: url,
               dataType: 'json',
               data: "",
               success: onSuccess,
               error: onError
           });
}

function appendByJSON(oldest_tid){
    is_processing = true;
    getUserGelo("/get_user_gelo.json?account=" + account + '&before_tid=' + oldest_tid);
}

function startByJSON(){
    $("#append").css('display', 'none');
    is_processing = true;
    $("#timeline").empty();
    geloDataGroup.removeAll();
    oldest_tid = 0;
    account = $("#account").val();    

    getUserGelo("/get_user_gelo.json?account=" + account);
}

$(document).keypress(function(event) {
                         if(event.target == document.getElementById("account")){
                             return;
                         }
                         var up_key = 107; // k
                         var down_key = 106; //j
                         var pressed_key = event.which;
                         if(pressed_key == up_key){
                             debug("up");
                             event_up();
                         }
                         if(pressed_key == down_key){
                             debug("down");
                             if(!event_down()){
                                 if(!is_processing){
                                     appendByJSON(oldest_tid);                                     
                                 }
                             }
                         }
                     });

$(document).ready(function(){
                      geloDataGroup = GeloDataGroup();
                      if($.query.get('debug')){
                          debug_enable = true;
                      }
                      account = $.query.get('account');
                      if(account){
                          $("#account").val(account);    
                          startByJSON();                          
                      }
                  });
