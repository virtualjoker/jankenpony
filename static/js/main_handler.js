// main_handler.js
//
// It will implements the responses handler

main.handler = {
  response: function(response){
    // Check if exist a token in this response
    
    if (typeof response.player != 'undefined'){
      main.out('handler.message player:'+dump(response.player));
      main.data.player = response.player;
    }
    
    if (typeof response.token != 'undefined'){
      main.channel.open(response.token);
    }
    
    if (typeof response.messages != 'undefined'){
      if (response.messages.length>0){
        for (var i in response.messages){
        main.out(response.messages[i], 'message');
        }
      }
    }
    
    if (typeof response.game_match != 'undefined'){
      main.out('handler.message game_match:'+dump(response.game_match));
      this.game_match(response.game_match);
    }
    
  },
  // GAME MATCH HANDLER
  game_match: function(game_match){
    
    
    if (typeof main.data.matches[game_match.game] == 'undefined'){
      main.data.matches[game_match.game] = game_match;
      main.screen.new_match(game_match);
    }
    else {
      // Check if it is a new match of the some created matc_game
      if (game_match.number != main.data.matches[game_match.game].number){
        // It is a new match, check if last match of this game
        // has finished yet, if it don't, force to remove it
        main.screen.remove_match(main.data.matches[game_match.game]);
        main.data.matches[game_match.game] = game_match;
        main.screen.new_match(game_match);
      }
    }
    
    // We already have this match o the screen,
    // now we just check for updates
    if (game_match.match_round > 0){
      main.screen.update_match_round(game_match);
      main.screen.show_choses(game_match);
    }
    
    
    
    // If it is the last match
    if(game_match.match_round == 3){
      // This game finished, and will be removed from screen and data
      main.screen.remove_match(game_match);
      delete main.data.matches[game_match.game];
    }
  },
};
