$(function () {
    $('div#editor_side_bar').hide();

    $('#wmd-input').focus(function(){ $('div#editor_side_bar').fadeIn('slow') });
    $('#wmd-input').blur(function(){ $('div#editor_side_bar').fadeOut('slow') });
});
