// main_screen.js
//
// It will implements how response will be show,
// creating matchs, etc.

function blink(element){
  element.animate({ borderWidth: "2px", margin: "10px" }, 'fast' )
        .animate({ borderWidth: "0px", margin: "12px" }, 'fast' )
        .animate({ borderWidth: "2px", margin: "10px" }, 'fast' )
        .animate({ borderWidth: "0px", margin: "12px" }, 'fast' )
        .animate({ borderWidth: "2px", margin: "10px" }, 'fast' )
        .animate({ borderWidth: "0px", margin: "12px" }, 'fast' )
        .animate({ borderWidth: "2px", margin: "10px" }, 'fast' )
        .animate({ borderWidth: "0px", margin: "12px" }, 'fast' )
        .animate({ borderWidth: "2px", margin: "10px" }, 'fast' )
        .animate({ borderWidth: "0px", margin: "12px" }, 'fast' )
}

main.screen = {
  //////////////////
  // REMOVE MATCH //
  //////////////////
  
  images: {
    player: $('<img />').attr('src', 'player.png'),
    challenger: $('<img />').attr('src', 'challenger.png'),
    stone_32px: $('<img />').attr('src', 'stone_32px.png'),
    paper_32px: $('<img />').attr('src', 'paper_32px.png'),
    scissors_32px: $('<img />').attr('src', 'scissors_32px.png'),
  },
  
  remove_match: function(game_match){
    match_div = $('#match_'+game_match.game.id)
    if (match_div){
      text = 'MATCH FINISHED';
      // THIS FUNCTION TO EXIBE THIS MESSAGE SHOULD BE MOVED
      // TO A NEW FUNCTION SCREEN.END_GAME
      // NEXT LINE NOT IMPLEMENTED RIGHT YET, BUT WILL NOT PLAY
      if (game_match.game.match_round == 4){
        text = 'MATCH DRAWS';
        if (typeof game_match.winner != 'undefined'){
          if (game_match.winner == main.data.player.id)
            text = 'YOU WIN';
          else if (game_match.loser == main.data.player.id)
            text = 'YOU LOSE';
        }
        
        gray_div = $('<div/>', {  
          class: 'gray_div',
          text: text,
        });
        gray_div.appendTo(match_div);
        gray_div.delay(3000).fadeIn('slow');
      }
      else{
        gray_div = $('<div/>', {  
          class: 'red_div',
          text: 'This match number didn\'t finish right.',
        });
        gray_div.appendTo(match_div);
        gray_div.delay(6000).fadeIn('slow');
      }
      
      //$('.my_choses').children().unbind();
      
      match_div.delay(9000)
        .fadeOut('slow', function() {
          $(this).remove();
        });
      
    }
  },
  
  
  ////////////////////////
  // UPDATE MATCH ROUND //
  ////////////////////////
  
  update_match_round: function(game_match){
    match_round = game_match.game.match_round;
    if (match_round == 4)
      match_round = 'END';
    $('#match_'+game_match.game.id+' > .round').fadeOut('fast', function() {
        $(this).html(match_round).fadeIn('fast');
      });
    
  },
  
  
  /////////////////
  // SHOW CHOSES //
  /////////////////
  
  show_choses: function(game_match){ // NOT REVIEWD YED
    main.out('screen.show_chose.game: '+game_match.game.id);
    
    
    $('#match_'+game_match.game.id+' > .choses > img').stop().css("borderWidth", "0px");
    
    
    player_last_choice = game_match.player.shots.pop()
    
    main.out('player_last_choice = '+player_last_choice);
    
    switch (player_last_choice){
      case 'nothing':
        blink($( ".player_choses > .rock_image" ));
        blink($( ".player_choses > .paper_image" ));
        blink($( ".player_choses > .scissors_image" ));
        break;
      case 'rock':
        blink($( ".player_choses > .rock_image" ));
        break;
      case 'paper':
        blink($( ".player_choses > .paper_image" ));
        break;
      case 'scissors':
        blink($( ".player_choses > .scissors_image" ));
        break;
    }
    
    challenger_last_choice = game_match.challenger.shots.pop()
    
    main.out('challenger_last_choice = '+challenger_last_choice);
    
    switch (challenger_last_choice){
      case 'nothing':
        blink($( ".challenger_choses > .rock_image" ));
        blink($( ".challenger_choses > .paper_image" ));
        blink($( ".challenger_choses > .scissors_image" ));
        break;
      case 'rock':
        blink($( ".challenger_choses > .rock_image" ));
        break;
      case 'paper':
        blink($( ".challenger_choses > .paper_image" ));
        break;
      case 'scissors':
        blink($( ".challenger_choses > .scissors_image" ));
        break;
    }
      
  },
  
  
  ///////////////
  // NEW MATCH //
  ///////////////
  
  new_match: function(game_match){
    main.out('screen.game_match.game.id: '+dump(game_match.game.id));
    
    matchs = $('#matchs');
    
    match_div = $('<div/>', {  
      id: 'match_'+game_match.game.id,
      class: 'match',
    });
    
    
    game_name = $('<div/>', {  
      class: 'name',
      text: game_match.game.name+' #'+game_match.game.match_counter,
    });
    game_name.appendTo(match_div);
    
    game_datetime = $('<div/>', {  
      class: 'datetime',
      text: 'match number: #'+game_match.game.match_counter+
            ' - '+game_match.game.datetime,
    });
    game_datetime.appendTo(match_div);
    
    player_image = $('<img/>', {  
      class: 'player_image',
      src: '/player.png', // Here comes the Player.img
    });
    player_image.appendTo(match_div);
    
    
    challenger_image = $('<img/>', {  
      class: 'challenger_image',
      src: '/challenger.png', // Here comes the Challenger.img
    });
    challenger_image.appendTo(match_div);
    
    
    match_round = $('<div/>', {  
      class: 'round',
      text: game_match.game.match_round,
    });
    match_round.appendTo(match_div);
    
    
    player_choses_div = $('<div/>', {  
      class: 'player_choses choses',
    });
    
    challenger_choses_div = $('<div/>', {  
      class: 'challenger_choses choses',
    });
    
    
    
    ///////////////////
    // PLAYER CHOSES //
    ///////////////////
    stone_image = this.images.stone_32px;
    stone_image.addClass('stone_image').click(function(){
      main.action.send('shot', [game_match.game.slug, 'rock']);
      
      $('#match_'+game_match.game.id+' > .player_choses > img').stop().css("borderWidth", "0px");
      
      $(this).animate({
        borderWidth: '6px',
        margin: '6px',
      }, 'fast', function() {
        
        $(this).animate({
        borderWidth: '2px',
        margin: '10px',
          }, 'fast');
        
      });
      
    });
    stone_image.appendTo(player_choses_div);
    
    
    
    paper_image = this.images.paper_32px;
    paper_image.addClass('paper_image').click(function(){
      main.action.send('shot', [game_match.game.slug, 'paper']);
       
      $('#match_'+game_match.game.id+' > .player_choses > img').stop().css("borderWidth", "0px");
      
      $(this).animate({
        borderWidth: '6px',
        margin: '6px',
      }, 'fast', function() {
        
        $(this).animate({
        borderWidth: '2px',
        margin: '10px',
          }, 'fast');
        
      });
      
    });
    paper_image.appendTo(player_choses_div);
    
    scissors_image = this.images.scissors_32px;
    scissors_image.addClass('scissors_image').click(function(){
      main.action.send('shot', [game_match.game.slug, 'scissors']);
      
      $('#match_'+game_match.game.id+' > .player_choses > img').stop().css("borderWidth", "0px");
      
      $(this).animate({
        borderWidth: '6px',
        margin: '6px',
      }, 'fast', function() {
        
        $(this).animate({
        borderWidth: '2px',
        margin: '10px',
          }, 'fast');
        
      });
      
    });
    scissors_image.appendTo(player_choses_div);
    
    
    
    ///////////////////////
    // CHALLENGER CHOSES //
    ///////////////////////
    
    stone_image2 = this.images.stone_32px;
    stone_image2.addClass('stone_image').click(function(){
      main.out('This is your challenger rock!', 'alert');
      
      $(this).animate({
        borderWidth: '2px',
        margin: '10px',
      }, 'fast', function() {
        $(this).animate({
          borderWidth: '0px',
          margin: '12px',
        }, 'fast');
      });
      
    });
    stone_image2.appendTo(challenger_choses_div);
    
    paper_image2 = this.images.paper_32px;
    paper_image2.addClass('paper_image').click(function(){
      main.out('This is your challenger rock!', 'alert');
      
      $(this).animate({
        borderWidth: '2px',
        margin: '10px',
      }, 'fast', function() {
        $(this).animate({
          borderWidth: '0px',
          margin: '12px',
        }, 'fast');
      });
      
    });
    paper_image2.appendTo(challenger_choses_div);
    
    
    scissors_image2 = this.images.scissors_32px;
    scissors_image2.addClass('scissors_image').click(function(){
      main.out('This is your challenger rock!', 'alert');
      
      $(this).animate({
        borderWidth: '2px',
        margin: '10px',
      }, 'fast', function() {
        $(this).animate({
          borderWidth: '0px',
          margin: '12px',
        }, 'fast');
      });
      
    });
    scissors_image2.appendTo(challenger_choses_div);
    
    // ADDING THE CHOSES DIV
    player_choses_div.appendTo(match_div);
    challenger_choses_div.appendTo(match_div)
    
    
    match_div.appendTo(matchs);
  },
  
};
