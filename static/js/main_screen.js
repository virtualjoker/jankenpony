// main_screen.js
//
// It will implements how response will be show,
// creating matchs, etc.

main.screen = {
  new_match: function(new_match){
    main.out('screen.new_match: '+dump(new_match.id));
    
    matchs = $('#matchs');
    new_match_div = $('<div/>', {  
      id: 'match_'+new_match.id,
      class: 'new_match',
      text: "Click me!",
    });
    
    player1_image = $('<img/>', {  
      class: 'player1_image',
      src: '/player1.png', // Here comes the P1 img
    });
    player1_image.appendTo(new_match_div);
    
    player2_image = $('<img/>', {  
      class: 'player2_image',
      src: '/player2.png', // Here comes the P2 img
    });
    player2_image.appendTo(new_match_div);
    
    
    
    rock_image = $('<img/>', {  
      class: 'rock_image',
      src: '/rock.png',
      click: function(){
        main.action.send('shot', [new_match.id, 'rock']);
        $(this).animate({
          border: '1px solid red',
          left: '+=62',
        }, 'fast', function() {
          main.out('You chose ROCK!');
          $(this).unbind('click');
        });
      },
    });
    rock_image.appendTo(new_match_div);
    
    paper_image = $('<img/>', {  
      class: 'paper_image',
      src: '/paper.png',
      click: function(){
        main.action.send('shot', [new_match.id, 'paper']);
        $(this).animate({
          border: '1px solid red',
          left: '+=62',
        }, 'fast', function() {
          main.out('You chose ROCK!');
          $(this).unbind('click');
        });
      },
    });
    paper_image.appendTo(new_match_div);
    
    scissors_image = $('<img/>', {  
      class: 'scissors_image',
      src: '/scissors.png',
      click: function(){
        main.action.send('shot', [new_match.id, 'scissors']);
        $(this).animate({
          border: '1px solid red',
          left: '+=62',
        }, 'fast', function() {
          main.out('You chose ROCK!');
          $(this).unbind('click');
        });
      },
    });
    scissors_image.appendTo(new_match_div);
    
    
    new_match_div.appendTo(matchs);
    main.out('Just testing to it!');
  },
};
