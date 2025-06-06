$(document).ready(()=>{
    setTimeout(()=>{
        const socket = new WebSocket((window.location.protocol=="http:"?"ws://":"wss://")+window.location.host+"/afk/ws");
        socket.onopen = function(event) {
            $("#wsStt").html("Connected.")
          };
        socket.onmessage = function(event) {
            e = JSON.parse(event.data.replaceAll("'","\""))
            $("main .info .bar .chb").css("width",`${e.time/e.totalTime*100}%`)
            $("#crvd").html(e.coin)
            $("#St").html(e.totalTime)
            $("#crv").html(e.crv)
        };
        socket.onclose = function(event) {
            $("#wsStt").html("Disconnected.")
            $("main .info .bar .chb").css("width",`0%`)
        };
    }, 2000)
})