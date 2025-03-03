import db
import json
import ende
import dns.resolver
import random
import time
import requests

with open("config.json","r", encoding="utf-8") as f:
    config = json.load(f)
pteroHost = config["pterodactyl"]["host"]
pteroKey = config["pterodactyl"]["key"]

_chr = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321"

def genSID():
    return "s."+"".join(random.choice(_chr) for i in range(random.randint(60, 90)))

def addSID(sid, user):
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("insert into session (sid, passport, alive) values (?, ?, ?)", (sid, user, time.time()+86400*15))
    conn.commit()
    conn.close()

def login(user, passwd):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("select * from user where user=?", (user,))
    result = cursor.fetchall()
    conn.close()
    if len(result) == 0:
        return (False, "Invalid username or password.")
    if not ende.checkpw(result[0][1], passwd):
        return (False, "Invalid username or password.")
    sid = genSID()
    addSID(sid, user)
    return (True, sid)

def register(user, passwd, email, cpu, ram, disk, slot, coin):
    conn = db.connect()
    cursor = conn.cursor()
    passwd = ende.encode(passwd)
    cursor.execute("select * from user where email=?", (email,))
    result = cursor.fetchall()
    if len(result) != 0:
        return (False, "Email has been used.")
    try:
        cursor.execute("insert into user (user, password, email, cpu, ram, disk, slot, coin) values (?, ?, ?, ?, ?, ?, ?, ?)", (user, passwd, email, cpu, ram, disk, slot, coin))
    except Exception:
        return (False, "Username has been used.")
    conn.commit()
    conn.close()
    return (True,)

def logout(sid):
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("delete from session where sid=?",(sid,))
    conn.commit()
    conn.close()

def chSID(sid):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("select * from session where sid=?",(sid,))
    result = cursor.fetchall()

    if len(result) == 0:
        return (False,)
    else:
        if (float(result[0][2]) < time.time()):
            logout(sid)
            return (False,)
        cursor.execute("select * from user where user=?",(result[0][1],))
        result = cursor.fetchall()
        result = {
            "user": result[0][0],
            "slot": result[0][3],
            "cpu": result[0][4],
            "disk": result[0][5],
            "ram": result[0][6],
            "coin": result[0][7]
        }
        return (True, result)

# print(chSID("s.CXToSbBpWYIVjc5aoYQILtYpU62iPsfjJFuxizGmrvNGktD6TZ63zUMLDWJVulo"))

# pteroHeader
headers = {
  'Authorization': f'Bearer {pteroKey}',
  'Content-Type': 'application/json',
  'Accept': 'Application/vnd.pterodactyl.v1+json'
}
# pteroHeader

def checkPteroUser(name):
    resp = requests.get(pteroHost+"/api/application/users?per_page=9999", headers=headers).json()
    if (resp.get("errors")): return (False, resp["errors"][0])
    else:
        for i in (resp["data"]):
            if i["attributes"]["username"] == name:
                return (True, i["attributes"])
        return (False, "nf")

def listPteroServer(name):
    userData = checkPteroUser(name)
    resp = requests.get(pteroHost+"/api/application/servers?per_page=9999", headers=headers).json()
    
    if (resp.get("errors")): return (False, resp["errors"][0])
    if (userData[0] == False): return (False, "usernf")
    
    uid = userData[1]["id"]
    uDt = []
    tCPU = 0
    tDisk = 0
    tRam = 0

    for i in resp["data"]:
        if i["attributes"]["user"] == uid:
            uDt.append(i["attributes"])
            tCPU += i["attributes"]["limits"]["cpu"]
            tRam += i["attributes"]["limits"]["memory"]/1024
            tDisk+= i["attributes"]["limits"]["disk"]/1024
    return (True, uDt, tCPU, tDisk, tRam)

# print(listPteroServer("h3l2f"))

def chMX(domain):
    try:
        r = dns.resolver.resolve(domain, "MX")
    except Exception:
        return 0
    else: return len(r)
