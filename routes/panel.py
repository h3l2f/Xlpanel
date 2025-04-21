# type: ignore
from __main__ import *

@app.route("/panel/<a>")
def gtpn(a:str=None):
    if a: return redirect(config["pterodactyl"]["host"]+f"/server/{a}")
    return redirect(config["pterodactyl"]["host"])