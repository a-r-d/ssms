/***
 *
 * User pages javascript.
 *
 *  
 */
if(!window.console) {
    window.console = {
        log: function() {},
        error: function() {}
    }
    alert('Please use chrome, IE blows');
}

function SSMSPlayer(options) {
    this.options = options;
    if(!options.playerId) {
        throw new Error('No player ID set');
    }
    if(!options.songSrcId) {
        throw new Error('No song source ID set');
    }

    this.playing_song_name = null;
    this.playing_song_path = null;
    this.context = null;
}

SSMSPlayer.prototype.updatePlayer = function(filePath){
    $(this.options.songSrcId).empty().append(filePath); //playing_song_name ); 
}

SSMSPlayer.prototype.playSong = function() {
    $(this.options.playerId).play();
    //document.getElementById("audio_control").play();
}

SSMSPlayer.prototype.pauseSong = function() {
    $(this.options.playerId).pause();
    // document.getElementById("audio_control").pause();
}

SSMSPlayer.prototype.reloadSong = function() {
    $(this.options.playerId).load();
    //doc
    ument.getElementById("audio_control").load();
}
SSMSPlayer.prototype.playFile = function( play_file ) {
    var self = this;
    console.log("Playing file: " + play_file);
    var req_name = encodeURIComponent(play_file);
    $(this.options.songSrcId).attr("src", "/file?q=" + req_name); //play_file has a prefixed slash
    $(this.options.songSrcId).data('songpath', play_file);

    try {
        self.reloadSong();
        self.playSong();
        
        var splits = play_file.replace("\\", "/").split("/");
        var name = splits[ splits.length - 1];
        self.playing_song_name = name;
        self.playing_song_path = play_file;
        
        self.updatePlayer( play_file );
    } catch ( e ) {
        console.error(e);
        alert( e );
    }
}

SSMSPlayer.prototype.playFileClick = function(play_file, context) {
    if( context != '' ) {
        this.context = context;
        console.log("Player context: " + context);
    }
    this.playFile( play_file )
}


var SSMS = {
    player: null,
    playing_song_name: null,
    playing_song_path: null,

    init: function(){
        var _player = new SSMSPlayer({
            songSrcId: '#song_src',
            playerId: '#audio_control',
            queryInput: '#query',
        });
        SSMS.player = _player;
    }
};
SSMS.init();

var playing_song_name = "";
var playing_song_path = "";
var playing_song_dir = "";
var current_browsed_dir = "/";
var dir_file_listing = [];
var player_context = ""; // ['browser', 'search', 'random', 'playlist']

var CONTEXT_RANDOM = "random";
var CONTEXT_SEARCH = "search";
var CONTEXT_BROWSER = "browser";
var CONTEXT_PLAYLIST = "playlist";

function utf8_to_b64( str ) {
  return window.btoa(unescape(encodeURIComponent( str )));
}

function b64_to_utf8( str ) {
  return decodeURIComponent(escape(window.atob( str )));
}
 
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

function updatePlayer( play_file_path ){
    $("#nowplaying").empty().append( play_file_path ); //playing_song_name ); 
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
    var req_name = encodeURIComponent(play_file);
    $("#song_src").attr("src", "/file?q=" + req_name); //play_file has a prefixed slash
    $("#song_src").data('songpath', play_file);

    try {
        document.getElementById("audio_control").load();
        document.getElementById("audio_control").play();
        
        var splits = play_file.replace("\\", "/").split("/");
        var name = splits[ splits.length - 1];
        
        playing_song_name = name;
        playing_song_path = play_file;
        
        updatePlayer( play_file );
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
    if( player_context == CONTEXT_RANDOM) {
        getRandom();
        return;
    }

    if( arr_to_iter.length < 2 ) {
        return;
    }
    console.log("Playing next song");

    var currFile = $("#song_src").data('songpath');
    for( var i = 0; i < arr_to_iter.length; i++) {
        if( currFile.indexOf( arr_to_iter[i].safePath ) != -1 ) {
            if(arr_to_iter.length - 1 > i ) {
                // play next
                playFile( arr_to_iter[i + 1].safePath );
                break;
            } else {
                // play first
                playFile( arr_to_iter[0].safePath );
                break;
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
    }*/
    
    if( arr_to_iter.length < 2 ) {
        return;
    }
    console.log("Playing previous song");
    var currFile = $("#song_src").data('songpath');
    for( var i = 0; i < arr_to_iter.length; i++) {
        if( currFile.indexOf( arr_to_iter[i].safePath ) != -1 ) {
            if(i != 0) {
                // play next
                 playFile( arr_to_iter[i - 1].safePath );
                 break;
            } else {
                // play first
                 playFile( arr_to_iter[0].safePath );
                 break;
            }
        }
    }
}

function songEnded() {
    console.log("song ended");
    nextSong();
}

function toggleRandom(){
    if( player_context == CONTEXT_RANDOM ) {
        player_context = "";
        $("#btn_random_toggle").removeClass("btn-success");
    } else {
        player_context = CONTEXT_RANDOM;
        getRandom();
        $("#btn_random_toggle").addClass("btn-success");
    }
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

function reloadDir() {
    loadDir( current_browsed_dir );
}

function loadDir( directory_name ) {    
    console.log("loading: " + directory_name );
    
    //var req_name = utf8_to_b64(directory_name);
    var req_name = encodeURIComponent(directory_name);
    console.log("Encoded: ", req_name);

    // Get the HTML from the template
    $.ajax({
        url: "/dir",
        dataType:"html",
        type: 'POST',
        data: {
            q: req_name
        },
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
        url: "/dir/json",
        dataType:"json",
        type: 'POST',
        data: {
            q: req_name
        },
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

function deleteTheFile( src ) {
    var yes_ok = confirm("Are you sure?");
    if (yes_ok){
        $.ajax({
            url: "/file/delete",
            data: {
                name: src
            },
            dataType:"html",
            success: function(result) {
                if( result == "ok" ) {
                    // reload dir
                    reloadDir();
                } else {
                    alert( result );
                }
            },
            error: function(result) {
                console.log("/files/delete There was some error: " + result);
                alert(result);
            }
        });
    }
}

function deleteTheDir( src ) {
    var yes_ok = confirm("Are you sure?");
    if (yes_ok){
        $.ajax({
            url: "/dir/delete",
            data: {
                name: src
            },
            dataType:"html",
            success: function(result) {
                if( result == "ok" ) {
                    // reload dir
                    reloadDir();
                } else {
                    alert( result );
                }
            },
            error: function(result) {
                console.log("/dir/delete There was some error: " + result);
                alert(result);
            }
        });
    }
}

///////////////////////////////////////////////////////////////////
/////////// boomarks                  /////////////////////////////

function createBookmark( src ) {
    var b_name =prompt("Please enter a name for the bookmark...","");
    if (b_name != null && b_name != ""){
        $.ajax({
            url: "/bookmark/new",
            data: {
                location: src,
                name: b_name
            },
            dataType:"html"
        }).done( function( res ) {
            if( res != "fail") {
                $('#bookmark_area').empty();
                $('#bookmark_area').append( res );
            } else {
                alert("Failure - check logs.")
            }
        }).fail( function( res ){
            console.log("/bookmark/new There was some error: " + res);
            alert(result);
        });
    }
}

/***
    Calls load dir on a selected bookmark.
    Should auto play on result. 
**/
function loadBookmark( src ) {
    loadDir( src );
}


function delBookmark( id ) {
    $.ajax({
        url: "/bookmark/del",
        data: {
            id: id
         },
        dataType:"html",
    }).done( function( res ) {
        if( res == "fail") {
            alert("Failure - check logs.")
        }
    }).fail( function( res ){ 
        console.log("/bookmark/del There was some error: " + res);
        alert(result);
    });
}

///////////////////////////////////////////////////////////////////
//////////////////       plylist     //////////////////////////////

function newPlaylist() {
    var b_name = prompt("New Playlist Name...","");
    if (b_name != null && b_name != ""){
        $.ajax({
            url: "/playlist/new",
            data: {
                name: b_name
            },
            dataType:"html"
        }).done( function( res ) {
            if( res != "fail") {
                $('#playlist_area').empty();
                $('#playlist_area').append( res );
            } else {
                alert("Failure - check logs.")
            }
        }).fail( function( res ){
            console.log("/playlist/new There was some error: " + res);
            alert(result);
        });
    }
}

function playPlaylist(id) {

}
function delPlaylist(id){

}
function delPlaylistItem(id, playlist_id) {
    $.ajax({
        url: "/playlist/item/del",
        data: {
            id: id,
            playlist_id: playlist_id
        },
        dataType:"html"
    }).done( function( result ) {
        if( result != "fail") {
            $('#edit_playlist_body').empty();
            $('#edit_playlist_body').append( result );
        } else {
            alert("Failure - check logs.")
        }
    }).fail( function( result ){
        console.log("/playlist/item/del There was some error: " + result);
        alert(result);
    });
}
function editPlaylist(id){
    $.ajax({
        url: "/playlist/edit/" + id,
        dataType:"html"
    }).done( function( result ) {
        if( result != "fail") {
            $('#edit_playlist_body').empty();
            $('#edit_playlist_body').append( result );
        } else {
            alert("Failure - check logs.")
        }
    }).fail( function( result ){
        console.log("/playlist/menu There was some error: " + result);
        alert(result);
    });

    $('#playlist_editor_modal').modal('show');
}
function addToPlaylist( src ){

    $.ajax({
        url: "/playlist/menu",
        data: {
            id: src
        },
        dataType:"html"
    }).done( function( res ) {
        if( res != "fail") {
            $('#list_playlist_body').empty();
            $('#list_playlist_body').append( res );
        } else {
            alert("Failure - check logs.")
        }
    }).fail( function( res ){
        console.log("/playlist/menu There was some error: " + res);
        alert(result);
    });

    $('#playlist_picker_modal').modal('show');
    $('#target-song').empty().append(src);
}

function addToPlaylistConfirm() {
    var src = $('#target-song').text();
    var id_list = [];
    // get all checked.
    $(".playist_checkbox").each( function( index ) {
        var checkbox = $(this);
        if( checkbox.prop('checked') || checkbox.prop('checked') == "checked" ){
            var id = checkbox.attr('id').split("_")[1];
            id_list.push( id );
        }
    });

    if(id_list.length > 0) {
        $('#loader_img_picker').show();
    }

    for( var i = 0; i < id_list.length; i++ ) {
        $.ajax({
            url: "/playlist/item/add",
            data: {
                id: id_list[i],
                path: src,
                list_order: 100
            },
            dataType:"html"
        }).done( function( res ) {
            if( res != "fail") {
                console.log( res );
            } else {
                alert("Failure - check logs.")
            }
            $('#loader_img_picker').hide();
        }).fail( function( res ){
            console.log("/playlist/item/add There was some error: " + res);
            alert(result);
            $('#loader_img_picker').hide();
        });
    }
}

////////////////////////////////////////////////////////////////////
function showAdmin(){
    var w = window.open("/admin", "Admin Panel", "width=500,height=700,left=200,top=100");
}

