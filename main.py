from flask import * #pyright:ignore
from flask_sock import Sock
import os
from werkzeug.exceptions import HTTPException
import helper
import datetime
import sendmail

app = Flask(__name__, template_folder="templates", static_folder="statics")
sock = Sock(app)
app.jinja_env.globals.update(list=list)
app.jinja_env.globals.update(datetime=datetime)
app.jinja_env.globals.update(request=request)

app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 2}

with open("config.json","r", encoding="utf-8") as f:
    config = json.load(f)

# general
name = config["name"]
ver = config["version"]
codename = config["codename"]
pcolor = config["color"]["primary"]
bcolor = config["color"]["background"]
tcolor = config["color"]["text"]

# flask
host = config["flask"]["host"]
port = config["flask"]["port"]
flaskDebug = config["flask"]["debug"]

# default
dft = {
    "cpu": config["default"]["cpu"],
    "ram": config["default"]["ram"],
    "disk": config["default"]["disk"],
    "slot": config["default"]["slot"],
    "coin": config["default"]["coin"]
}

# list
eggsList = config["eggs"]
nodeList = config["locations"]

# menu
menuItems = {
    "Dashboard": {
        "link": "/dashboard",
        "icon": "<i class=\"fa-solid fa-house\"></i>"
    },
    "Server": {
        "link": "/servers",
        "icon": """<i class="fa-solid fa-server"></i>"""
    },
    "Store": {
        "link": "/store",
        "icon": """<i class="fa-solid fa-bag-shopping"></i>"""
    },
    "Afk": {
        "link": "/afk",
        "icon": """<i class="fa-solid fa-bullseye"></i>"""
    },
    "Account": {
        "link": "/account",
        "icon": """<i class="fa-solid fa-user"></i>"""
    }
}

# afk
afk = config["afk"]
store = config["store"]

routeFile = os.listdir("routes")
if not afk["enable"]:
    routeFile.remove("afkpage.py")
    routeFile.remove("afk_ws.py")
    menuItems.pop("Afk")
if not store["enable"]:
    routeFile.remove("store.py")
    menuItems.pop("Store")
if not config["mail"]["verifyUser"]:
    routeFile.remove("verify.py")
for i in routeFile:
    if "__" in i: continue
    exec(f"import routes.{i.split('.')[0]}")

if __name__ == "__main__":
    app.run(debug=flaskDebug, port=port, host=host)