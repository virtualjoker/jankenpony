// main.js
// 
// It implements the main javascript function

var main = {
  data: {
    player: {},
    matches: {},
  },
  start: function(event) {
    this.out('main.start');
    this.channel.start();
  },
  unload: function(event){
    this.out('game.unload');
    // It will close the Channel Socket. ??? PROBABILY!
  },
  error: function(event){
    this.out('game.error:');
    this.out('-- type:' + event.type);
    this.out('-- data:' + event.data);
  },
  out: function(text, type){
    // If this player accepts out msg
    if (!$('#out_active').attr('checked')){
      return;
    }
    
    if (!type)
      type = 'normal';
    
    switch (type){
      case 'normal':
        color = '#000000';
        background_color = '#cccccc';
        break;
      case 'message':
        text = 'Message: ' + text;
        color = '#00008b';
        background_color = '#cccccc';
        break;
      case 'alert':
        text = 'Alert: ' + text;
        color = '#ffff00';
        background_color = '#cccccc';
        break;
      case 'error':
        text = 'Error: ' + text;
        color = '#8b0000';
        background_color = '#cccccc';
        break;
      default:
        game.out('You cant send a message with type '+type, 'error')
        return;
    }
    $("<p/>", {
      text: text,
      css: {
        color: color,
        backgroundColor: background_color,
      },
      mouseenter: function(){
        $(this).fadeOut(
          'slow',
          function(){
            $(this).remove();
          }
        );
      },
    }).appendTo("#out");
  },
};

$(document).ready(
  function(event){
    main.start(event);
  }
);

$(window).error(
  function(event){
    main.error(event);
  }
);

$(window).unload(
  function(event){
    main.unload(event);
  }
);
