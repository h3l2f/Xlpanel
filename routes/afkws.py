# type: ignore
from __main__ import *

@sock.route('/afk/ws')
def echo(ws):
    print(request.headers.get("Authorization", "None"))
    while True:
        data = ws.receive()
        ws.send(data)