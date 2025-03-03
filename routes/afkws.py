# type: ignore
from __main__ import *

@sock.route('/afk/ws')
def echo(ws):
    print(request.cookies.get("sid"))
    while True:
        data = ws.receive()
        ws.send(data)