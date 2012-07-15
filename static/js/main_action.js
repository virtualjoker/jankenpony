// main_action.js
//
// It implements the function to send actions to server

main.action = {
  timeout: 10000, // Forcing to end the connection in 10s
  sendtime: 0, // It will be used to calculate the latency
  beforesend: function(XMLHttpRequest, settings){
    // Really dunno. ???
    main.out('action.beforesend setings:' + settings.data);
  },
  error: function(XMLHttpRequest, error){
    main.out('action.error error:' + error);
  },
  success: function(data, textStatus, XMLHttpRequest){
    main.out('action.sucess data:' + data);
    main.out('action.sucess textStatus:' + textStatus);
    main.out('action.sucess dump(data):' + dump(data));
    // Here we will handle the response DATA
    main.handler.response(data);
  },
  complete: function(XMLHttpRequest, textStatus){
    // "success", "notmodified", "error", "timeout", or "parsererror"
    completetime = new Date().getTime();
    latency = completetime - main.action.sendtime
    main.out('action.complete latency:' + latency);
    main.out('action.complete textStatus:' + textStatus);
  },
  // Here is an example how to call this function:
  // main.action.send('funcao_teste', ['up','down', 23452]);
  // never forget that the args is an Array of args
  // ALL EMPTY ARG WILL BE REMOVED ON THE HOST
  send: function(action, args){
    
    // To mensure the latency when this call finishes
    this.sendtime = new Date().getTime();
    
    // If optional arguments was not provided,
    // we have to create a empty array of args
    if (!args)
      args = new Array();
    
    // If optional arguments was just one string,
    // it must be transformed in an array
    if (typeof(args) == 'string')
      args = new Array();
    
    main.out('action.send action:' + action);
    main.out('action.send dump(args):' + dump(args));
    
    $.ajax({
      url: '/action', // All actions will be sent to /action url
      type: 'POST',
      cache: false,
      dataType: 'json',
      data: ({
        action: action,
        'args[]': args,
        //time: main.action.sendtime, // Not used for now
      }),
      timout: main.action.timeout,
      beforeSend: main.action.beforesend,
      error: main.action.error,
      success: main.action.success,
      complete: main.action.complete,
    });
  },
};
