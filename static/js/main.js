// main.js
// 
// It implements the main javascript function

var main = {
  data: {
    matchs: {},
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
  out: function(msg){
    
    color = '#000000';
    border_color = '#666';
    
    $("<p/>", {
      text: msg,
      css: {
        color: color,
        borderColor: border_color,
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
