// main_handler.js
//
// It will implements the responses handler

main.handler = {
  response: function(response){
    // Check if exist a token in this response
    if (typeof response.token != 'undefined'){
      main.channel.open(response.token);
    }
    
    if (typeof response.new_match != 'undefined'){
      main.out('handler.message new_match:'+dump(response.new_match));
      this.new_match(response.new_match);
    }
    
  },
  new_match: function(new_match){
    main.out('handler.new_match: '+dump(new_match.id));
    main.screen.new_match(new_match);
  },
};
