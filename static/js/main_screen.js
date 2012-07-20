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
  remove_match: function(game_match){
    match_div = $('#match_'+game_match.game)
    if (match_div){
      
      if (game_match.match_round == 3){
        text = 'MATCH FINISHED';
        if (game_match.winner != 'undefined'){
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
        gray_div.delay(3000).fadeIn('slow');
      }
      
      //$('.my_choses').children().unbind();
      
      match_div.delay(6000)
        .fadeOut('slow', function() {
          $(this).remove();
        });
      
    }
  },
  
  update_match_round: function(game_match){
    $('#match_'+game_match.game+' > .round').fadeOut('fast', function() {
        $(this).html(game_match.match_round);
        $(this).fadeIn('fast');
      });
    
  },
  
  show_choses: function(game_match){
    main.out('screen.show_chose.game: '+game_match.game);
    
    
    // SELECTING THE PLAYER AND THE CHALLENGER
    if (main.data.player.id == game_match.player1){
      player_last_choice = game_match.player1_choices.pop();
      challenger_last_choice = game_match.player2_choices.pop();
    }
    else if (main.data.player.id == game_match.player1){
      player_last_choice = game_match.player2_choices.pop();
      challenger_last_choice = game_match.player1_choices.pop();
    }
    else {
      main.out('You aren\'t in this match!', 'error');
      return
    }
    
    $('#match_'+game_match.game+' > .choses > img').stop().css("borderWidth", "0px");
    
    
    
    
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
  
  new_match: function(new_match){
    main.out('screen.new_match.game: '+dump(new_match.game));
    
    
    // SELECTING THE PLAYER AND THE CHALLENGER
    if (main.data.player.id == new_match.player1){
      player = new_match.player1
      challenger = new_match.player2
    }
    else if (main.data.player.id == new_match.player1){
      player = new_match.player2
      challenger = new_match.player1
    }
    else {
      main.out('You aren\'t in this match!', 'error');
      return
    }
    
    matchs = $('#matchs');
    
    match_div = $('<div/>', {  
      id: 'match_'+new_match.game,
      class: 'match',
    });
    
    player_image = $('<img/>', {  
      class: 'player_image',
      src: '/player.png', // Here comes the Player img
    });
    player_image.appendTo(match_div);
    
    challenger_image = $('<img/>', {  
      class: 'challenger_image',
      src: '/challenger.png', // Here comes the Challenger img
    });
    challenger_image.appendTo(match_div);
    
    
    match_round = $('<div/>', {  
      //id: 'round_'+new_match.game,
      class: 'round',
      text: new_match.match_round,
    });
    match_round.appendTo(match_div);
    
    
    player_choses_div = $('<div/>', {  
      //id: 'player_choses_'+new_match.game,
      class: 'player_choses choses',
    });
    
    challenger_choses_div = $('<div/>', {  
      //id: 'player2_choses_'+new_match.game,
      class: 'challenger_choses choses',
    });
    
    
    // ADDING MY CHOSES IMAGE IN MY_CHOSES DIV
    rock_image = $('<img/>', {  
      class: 'rock_image',
      src: '/rock.png',
      click: function(){
        main.action.send('shot', [new_match.game,  new_match.player1_status, new_match.player2_status, 'rock']);
        
        $('#match_'+new_match.game+' > .player_choses > img').stop().css("borderWidth", "0px");
        
        $(this).animate({
          borderWidth: '6px',
          margin: '6px',
        }, 'fast', function() {
          
          $(this).animate({
          borderWidth: '2px',
          margin: '10px',
            }, 'fast');
          
        });
        
      },
    });
    rock_image.appendTo(player_choses_div);
    
    paper_image = $('<img/>', {  
      class: 'paper_image',
      src: '/paper.png',
      click: function(){
        main.action.send('shot', [new_match.game,  new_match.player1_status, new_match.player2_status, 'paper']);
        
        $('#match_'+new_match.game+' > .player_choses > img').stop().css("borderWidth", "0px");
        
        $(this).animate({
          borderWidth: '6px',
          margin: '6px',
        }, 'fast', function() {
          
          $(this).animate({
          borderWidth: '2px',
          margin: '10px',
            }, 'fast');
          
        });
        
      },
    });
    paper_image.appendTo(player_choses_div);
    
    scissors_image = $('<img/>', {  
      class: 'scissors_image',
      src: '/scissors.png',
      click: function(){
        main.action.send('shot', [new_match.game,  new_match.player1_status, new_match.player2_status, 'scissors']);
        
        $('#match_'+new_match.game+' > .player_choses > img').stop().css("borderWidth", "0px");
        
        $(this).animate({
          borderWidth: '6px',
          margin: '6px',
        }, 'fast', function() {
          
          $(this).animate({
          borderWidth: '2px',
          margin: '10px',
            }, 'fast');
          
        });
        
      },
    });
    scissors_image.appendTo(player_choses_div);
    
    
    
    // CHALLENGER CHOSES IMAGE
    
    rock_image = $('<img/>', {  
      class: 'rock_image',
      src: '/rock.png',
      click: function(){
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
        
      },
    });
    
    rock_image.appendTo(challenger_choses_div);
    
    paper_image = $('<img/>', {  
      class: 'paper_image',
      src: '/paper.png',
      click: function(){
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
        
      },
    });
    paper_image.appendTo(challenger_choses_div);
    
    scissors_image = $('<img/>', {  
      class: 'scissors_image',
      src: '/scissors.png',
      click: function(){
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
        
      },
    });
    scissors_image.appendTo(challenger_choses_div);
    
    // ADDING THE CHOSES DIV
    player_choses_div.appendTo(match_div);
    challenger_choses_div.appendTo(match_div)
    
    
    match_div.appendTo(matchs);
  },
  
};
