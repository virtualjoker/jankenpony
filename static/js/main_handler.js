// main_handler.js
//
// It will implements the responses handler

main.handler = {
  response: function(response){
    // Check if exist a token in this response
    if (typeof response.token != 'undefined'){
      main.channel.open(response.token);
    }
    
  },
};
