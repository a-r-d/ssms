/***
 *
 * User pages javascript.
 *
 *  
 */
var playing_song_name = "";
var playing_song_path = "";
var playing_song_dir = "";
var current_browsed_dir = "";
var dir_file_listing = [];
var player_context = ""; // ['browser', 'search', 'random', 'playlist']

var CONTEXT_RANDOM = "random";
var CONTEXT_SEARCH = "search";
var CONTEXT_BROWSER = "browser";
var CONTEXT_PLAYLIST = "playlist";
 
$(document).ready( function(){

    $('#query_submit').click( function(e){
        e.preventDefault();
        doSearch();
    })

    $('#query_form').submit( function(e){
        e.preventDefault();
        doSearch();
    })

    $('#query').autocomplete({
      source: function( request, response ) {

        console.log("Performing search:");
        var search_term = $('#query').val();
        
        $.ajax({
          url: "/search/json",
          dataType: "json",
          data: {
            q: search_term
          },
          minLength: 3,
          success: function( data ) {
            console.log( data );
            response( $.map( data.files, function( item ) {
                console.log( item );
              return {
                label: item.name,
                value: item.name
              }
            }));
          }
        });
      }
    });
});

///////////////////////////////////////////////////////
// Click events:
///////////////////////////////////////////////////////

function updatePlayer(){
    $("#nowplaying").empty().append( playing_song_name ); 
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
    $("#song_src").attr("src", "/file?q=" + play_file); //play_file has a prefixed slash
    try {
        document.getElementById("audio_control").load();
        document.getElementById("audio_control").play();
        
        var splits = play_file.replace("\\", "/").split("/");
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
    if( context != '' ) {
        player_context = context;
        console.log("Player context: " + context);
    }
    playFile( play_file )
}

function nextSong() {
    var arr_to_iter = dir_file_listing;
    /*
    if( player_context == 'search' ) {
        arr_to_iter = search_file_array;
    } else if( player_context == 'playlist') {
        arr_to_iter = playlist_file_array;
    }
    */
    console.log("Playing next song");
    if( arr_to_iter.length < 2 ) {
        return;
    }
    var currFile = $("#song_src").attr("src");
    for( var i = 0; i < arr_to_iter.length; i++) {
        if( currFile.indexOf( arr_to_iter[i].safePath ) != -1 ) {
            if(arr_to_iter.length - 1 > i ) {
                // play next
                 playFile( arr_to_iter[i + 1].safePath )
            } else {
                // play first
                playFile( arr_to_iter[0].safePath )
            }
        }
    }
}

function prevSong() {
    var arr_to_iter = dir_file_listing;
    /*
    if( player_context == 'search' ) {
        arr_to_iter = search_file_array;
    } else if( player_context == 'playlist') {
        arr_to_iter = playlist_file_array;
    }
    */
    console.log("Playing previous song");
    if( arr_to_iter.length < 2 ) {
        return;
    }
    var currFile = $("#song_src").attr("src");
    for( var i = 0; i < arr_to_iter.length; i++) {
        if( currFile.indexOf( arr_to_iter[i].safePath ) != -1 ) {
            if(i != 0) {
                // play next
                 playFile( arr_to_iter[i - 1].safePath )
            } else {
                // play first
                 playFile( arr_to_iter[0].safePath )
            }
        }
    }
}

function songEnded() {
    console.log("song ended");
    nextSong();
}

function getRandom() {
    $.ajax({
        url: "/random",
        dataType:"text",
        success: function(result) {
           //console.log("Got random: " + result)
           playFile( result );
        },
        error: function(result) {
            console.log("/random There was some error: " + result);
            alert("error getting random file");
        }
    });
}

function doSearch() {
    var term = $('#query').val();
    if( term == "") return;

    $.ajax({
        url: "/search?q=" + term,
        dataType:"text",
        success: function(result) {
           //console.log("Got search: " + result)
           $("#file_browser_table").empty().append(result);
           current_browsed_dir = "";
           player_context = CONTEXT_SEARCH;
           updateBreadcrumbs();
        },
        error: function(result) {
            console.log("/random There was some error: " + result);
            alert("error getting random file");
        }
    });
}

function loadDir( directory_name ) {    
    console.log("loading: " + directory_name );
    
    // Get the HTML from the template
    $.ajax({
        url: "/dir?q=" + directory_name,
        dataType:"html",
        success: function(result) {
           $("#file_browser_table").empty().append(result);
           current_browsed_dir = directory_name;
           updateBreadcrumbs();
        },
        error: function(result) {
            console.log("/dir There was some error: " + result);
            alert("error getting files");
        }
    });
    
    // get the JSON 
    $.ajax({
        url: "/dir/json?q=" + directory_name,
        dataType:"json",
        success: function(result) {
           console.log( result );
           dir_file_listing = result;
        },
        error: function(result) {
            console.log("/dir/json There was some error: " + result);
        }
    });
}

function updateBreadcrumbs(){
    var cleaned = current_browsed_dir.replace("\\", "/").replace("//", "/"); // i want single forward slashes
    if( cleaned.substring(0,1) == "/" ) {
        cleaned = cleaned.substring(1); // break off the first piece.
    }
    
    var splits = cleaned.split("/");
    var no_empty = [];
    for( var i = 0; i < splits.length; i++) {
        if( splits[i] != "" && splits[i] != "." ) {
            no_empty.push( splits[i] );
        }
    }
    splits = no_empty;
    
    $("#dir_breadcrumb").empty();
    $("#dir_breadcrumb").append("/ <a href='javascript:void(0);' onClick='loadDir(\"/\")'>home</a> /");
    if( splits.length == 0 || (splits.length == 1 && splits[0] == "") ) return;
    for( var i = 0; i < splits.length; i++) {
        $("#dir_breadcrumb").append('<a href="javascript:void(0);" onClick=\'loadDir("' + addUp( splits, i) + '")\'>' + splits[i] + "</a> /");
    }
}

function addUp(arr, position){
    var str = "";
    if( arr.length >= position ) {
        for( var i=0; i < position + 1; i++) {
            str += arr[i] + "/";
        }
        return str;
    } else {
        return arr[0];
    }
}

function downloadFile( src ){
    window.open("/file/download?q=" + src, '_blank');
    window.focus();
}

function downloadNowPlaying(){
    // shold be this: playing_song_path
    window.open("/file/download?q=" + playing_song_path, '_blank');
    window.focus();
}

function downloadFolder( src ){
    window.open("/dir/download?q=" + src, '_blank');
    window.focus();
}

function uploadToLocation( src ){
    var w = window.open("/upload/form?q=" + src, "File Multi-Uploader!", "width=500,height=500,left=200,top=100");
    var watchClose = setInterval(function() {
        try {
            if (w.closed) {
             clearTimeout(watchClose);
             loadDir( src );
            }
        } catch (e) {}
     }, 100);
}

function makeNewDir( src ){
    var f_name =prompt("Please enter a new folder Name","");
    if (f_name != null && f_name != ""){
        $.ajax({
            url: "/newdir",
            data: {
                location: src,
                name: f_name
            },
            dataType:"html",
            success: function(result) {
                alert(result);
                loadDir( src );
            },
            error: function(result) {
                console.log("/newdir There was some error: " + result);
                alert(result);
            }
        });
    }
}

///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////


function showAdmin(){
    var w = window.open("/admin", "Admin Panel", "width=500,height=700,left=200,top=100");
}

