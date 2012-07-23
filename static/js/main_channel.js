// main_channel.js
//
// It will implements the channel handler

main.channel = {
  token: null, // Wen main.channel.stat() it will take it by action
  channel: null,
  socket: null,
  onopen: function(){
    main.out('channel.onopen');
  },
  onmessage: function(msg){
    main.out('channel.onmessage msg.data:' + msg.data);
    response = null;
    try{
      response = $.parseJSON(msg.data);
    }catch(e){
      main.out('CHANNEL ERROR parseJSON:"'+e+'"');
    }
    if (response){
      main.handler.response(response);
    }
  },
  onerror: function(msg){
    main.out('channel.onerror dump(msg)' + dump(msg));
  },
  onclose: function(){
    main.out('channel.onclose forcing to restart');
    // It closed for some rason, lets take another token and reopen it
    main.channel.token = null;
    main.channel.start();
  },
  open: function(token){
    main.out('channel.open');
    
    if (token){
      this.token = token;
    }
    
    this.channel = new goog.appengine.Channel(this.token);
    
    this.socket = this.channel.open({
      'onopen': main.channel.onopen,
      'onmessage': main.channel.onmessage,
      'onerror': main.channel.onerror,
      'onclose': main.channel.onclose
    });
    
    /* Maybe this lines isn't necessary
    this.socket.onopen = this.onopen;
    this.socket.onmessage = this.onmessage;
    this.socket.onerror = this.onerror;
    this.socket.onclose = this.onclose;
    */
  },
  close: function(){
    main.out('channel.close');
    //if (this.socket)
    // this.socket.close();
  },
  start: function(){
    main.out('channel.start');
    //main.action.send('get_token');
    if (this.token){
      this.open();
    }
    else{
      main.out('channel.start should take new token!');
      // there is a error in there
      main.action.send('get_token');
    }
  },
};
