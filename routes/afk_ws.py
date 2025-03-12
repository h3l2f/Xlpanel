# type: ignore
from __main__ import *
import time
import db

wsConnect = []

@sock.route('/afk/ws')
def echo(ws):
    check = helper.chSID(request.cookies.get("sid"))
    if (check[0]):
        if check[1]["user"] in wsConnect: return
        wsConnect.append(check[1]["user"])
        conn = db.connect()
        cursor = conn.cursor()
        coin = 0
        t=0
        try:
            while True:
                time.sleep(1)
                t+=1
                if (t==afk["stageTime"]):
                    t = 0
                    coin+=afk["coinPerStage"]
                    cursor.execute("update user set coin=coin+? where user=?", (afk["coinPerStage"], check[1]["user"]))
                    conn.commit()
                ws.send({"coin": coin, "totalTime": afk["stageTime"], "time": t, "crv": afk["coinPerStage"]})
        except Exception as e:
            conn.close()
            wsConnect.remove(check[1]["user"])
            print(e)