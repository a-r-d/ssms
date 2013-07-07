/***
 *
 * User pages javascript.
 *
 *  
 */
 
var playing_song_name = "";
var playing_song_path = "";
var playing_song_dir = "";
var player_context = ""; // ['browser', 'search', 'custom']
 
$(document).ready( function(){


});

///////////////////////////////////////////////////////
// Click events:
///////////////////////////////////////////////////////

function updatePlayer(){
    $("#nowplaying").empty().append(player_context + ": " + name ); 
    //$("#current_song").empty().append(player_context + ": " + name);
}

function playSong() {
    document.getElementById("audio_control").play();
}
function pauseSong() {
    document.getElementById("audio_control").pause();
}
function reloadSong() {
    document.getElementById("audio_control").load();
}

function playFile( play_file ) {
    // a hack:
    //play_file = play_file.replace("*", "'");
    console.log("Playing file: " + play_file);
    $("#song_src").attr("src", "/file" + play_file); //play_file has a prefixed slash
    try {
        document.getElementById("audio_control").load();
        document.getElementById("audio_control").play();
        
        var splits = play_file.split("/");
        var name = splits[ splits.length - 1];
        
        playing_song_name = name;
        playing_song_path = play_file;
        
        updatePlayer();
        
    } catch ( e ) {
        alert( e );
    }
}

// all click events have a context.
// other version of play file is ofter trigger via code.
function playFileClick(play_file, context) {
    if( context != 'auto' ) {
        player_context = context;
        console.log("Player context: " + context);
    }
    playFile( play_file )
}

function nextSong() {
    var arr_to_iter = file_array;
    if( player_context == 'search' ) {
        arr_to_iter = search_file_array;
    } else if( player_context == 'playlist') {
        arr_to_iter = playlist_file_array;
    }
    
    console.log("Playing next song");
    if( arr_to_iter.length < 2 ) {
        return;
    }
    var currFile = $("#song_src").attr("src");
    for( var i = 0; i < arr_to_iter.length; i++) {
        if( currFile == arr_to_iter[i]) {
            if(arr_to_iter.length - 1 > i ) {
                // play next
                 playFile( arr_to_iter[i + 1] )
            } else {
                // play first
                playFile( arr_to_iter[0] )
            }
        }
    }
}

function prevSong() {
    var arr_to_iter = file_array;
    if( player_context == 'search' ) {
        arr_to_iter = search_file_array;
    } else if( player_context == 'playlist') {
        arr_to_iter = playlist_file_array;
    }
    
    console.log("Playing previous song");
    if( arr_to_iter.length < 2 ) {
        return;
    }
    var currFile = $("#song_src").attr("src");
    for( var i = 0; i < arr_to_iter.length; i++) {
        if( currFile == arr_to_iter[i]) {
            if(i != 0) {
                // play next
                 playFile( arr_to_iter[i - 1] )
            } else {
                // play first
                 playFile( arr_to_iter[0] )
            }
        }
    }
}

function songEnded() {
    console.log("song ended");
    nextSong();
}

function loadDir( directory_name ) {    
    console.log("loading: " + directory_name );
    
    // a hack:
    //directory_name = directory_name.replace("*", "'");
    
    var dat = {
        dir: directory_name
    }
    $.ajax({
        url: "dir_list.php",
        data: dat,
        dataType:"json",
        success: function(result) {
           var table = result.table;
           var files = result.files;
           $("#dir_listing_table").empty().append(table);
           
           file_array = files;
           
           one_dir_up = getOneUp( directory_name )
        },
        error: function(result) {
            console.log("There was some error: " + result);
            alert("error getting files");
        }
    });
}
