# type: ignore
from __main__ import *

@app.route("/panel")
def gtpn():
    return redirect(config["pterodactyl"]["host"])