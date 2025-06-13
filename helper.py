import db
import json
import ende
import dns.resolver
import random
import time
import requests

from sendmail import sendVerify

with open("config.json","r", encoding="utf-8") as f:
	config = json.load(f)
pteroHost = config["pterodactyl"]["host"]
pteroKey = config["pterodactyl"]["key"]

# pteroHeader
headers = {
  'Authorization': f'Bearer {pteroKey}',
  'Content-Type': 'application/json',
  'Accept': 'Application/vnd.pterodactyl.v1+json'
}
# pteroHeader

_chr = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321"

def genSID():
	return "s."+"".join(random.choice(_chr) for i in range(random.randint(60, 90)))

def addSID(sid, user):
	sid = ende.hash(sid)
	conn = db.connect()
	cursor = conn.cursor()
	cursor.execute("insert into session (sid, passport, alive) values (?, ?, ?)", (sid, user, time.time()+86400*15))
	conn.commit()
	conn.close()

def createPteroUser(user, email):
	data = {
	"email": email,
	"username": user,
	"first_name": ".",
	"last_name": user
	}
	resp = requests.post(pteroHost+"/api/application/users",json=data, headers=headers)
	return resp.json()

def login(user, passwd):
	user = user.lower()
	conn = db.connect()
	cursor = conn.cursor()

	cursor.execute("select * from user where user=?", (user,))
	result = cursor.fetchall()
	conn.close()
	if len(result) == 0:
		return (False, "Invalid username or password.")
	if not ende.checkpw(result[0][1], passwd):
		return (False, "Invalid username or password.")
	if result[0][8]==0:
		conn = db.connect()
		cursor = conn.cursor()
		code = "".join(random.choice(_chr) for i in range(6))
		try:
			cursor.execute("insert into verify (user, email, code) values (?, ?, ?)", (result[0][0], result[0][2], code))
		except Exception:
			cursor.execute("select code from verify where user=?", (result[0][0],))
			code = cursor.fetchall()[0][0]
		conn.commit()
		conn.close()
		e = sendVerify(result[0][2], code)
		if e[0] == False:
			return (False, "Cannot send verify mail.")
		return (False, "verify", result[0][0])
	elif result[0][10]:
		return (False, "banned")
	sid = genSID()
	addSID(sid, user)
	return (True, sid)

def getUser(user):
	conn = db.connect()
	cursor = conn.cursor()
	cursor.execute("select * from user where user=?", (user,))
	result = cursor.fetchall()
	if not len(result): return (False, "User not found.")
	result = {
			"user": result[0][0],
			"slot": result[0][3],
			"cpu": result[0][4],
			"disk": result[0][5],
			"ram": result[0][6],
			"coin": result[0][7],
			"banned": result[0][10]
		}
	return (True, result)

def checkVcode(user, code):
	conn = db.connect()
	cursor = conn.cursor()
	cursor.execute("select * from verify where user=?", (user,))
	r = cursor.fetchall()
	
	if len(r) == 0:
		return (False, "User not found.")
	rcode = r[0][2]
	if code != rcode:
		return (False, "Invalid verify code!")
	sid = genSID()
	addSID(sid, user)
	cursor.execute("update user set verified=1 where user=?", (user,))
	cursor.execute("delete from verify where user=?", (user,))
	conn.commit()
	conn.close()
	createPteroUser(r[0][0], r[0][1])
	return (True, sid)

def register(user, passwd, email, cpu, ram, disk, slot, coin):
	for i in user:
		if i not in _chr.replace("ABCDEFGHIJKLMNOPQRSTUVWXYZ", ""):
			return (False, "Username must contain only lower-case characters and numbers.")
	user = user.lower().replace(" ", "")
	conn = db.connect()
	cursor = conn.cursor()
	passwd = ende.encode(passwd)
	cursor.execute("select * from user where email=?", (email,))
	result = cursor.fetchall()
	e = int(not config["mail"]["verifyUser"])
	if len(result) != 0:
		return (False, "Email has been used.")
	try:
		cursor.execute("insert into user (user, password, email, cpu, ram, disk, slot, coin, verified) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (user, passwd, email, cpu, ram, disk, slot, coin, e))
	except Exception:
		return (False, "Username has been used.")
	if not config["mail"]["verifyUser"]: createPteroUser(user, email)
	conn.commit()
	conn.close()
	return (True,)

def logout(sid):
	sid = ende.hash(sid)
	conn = db.connect()
	cursor = conn.cursor()
	cursor.execute("delete from session where sid=?",(sid,))
	conn.commit()
	conn.close()

def chSID(sid):
	conn = db.connect()
	cursor = conn.cursor()
	sid = ende.hash(sid)
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
		if result[0][10]:
			logout(sid)
			return (False, "banned")
		result = {
			"user": result[0][0],
			"pwd": result[0][1],
			"slot": result[0][3],
			"cpu": result[0][4],
			"disk": result[0][5],
			"ram": result[0][6],
			"coin": result[0][7],
			"banned": result[0][10]
		}
		return (True, result)

def checkPteroUser(name):
	resp = requests.get(pteroHost+"/api/application/users?per_page=9999", headers=headers).json()
	if (resp.get("errors")): return (False, resp["errors"][0])
	else:
		for i in (resp["data"]):
			if i["attributes"]["username"] == name:
				return (True, i["attributes"])
		return (False, "nf")

def getPteroAllocation(node_id, _random=False):
	resp = requests.get(pteroHost+f"/api/application/nodes/{node_id}/allocations?per_page=9999", headers=headers).json()
	if (resp.get("errors")): return (False, resp["errors"][0])
	r = resp["data"]
	i = 0
	while (r[i]["attributes"]["assigned"]):
		if _random: i = random.randint(0, len(r)-1)
		else:
			if (i == len(r)-1): return (False, )
			else: i+=1
	return (True, r[i]["attributes"])

def listPteroNode(name):
	resp = requests.get(pteroHost+"/api/application/nodes?per_page=9999", headers=headers).json()
	if (resp.get("errors")): return (False, resp["errors"][0])
	for i in (resp["data"]):
		if i["attributes"]["name"] == name:
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
			tRam += i["attributes"]["limits"]["memory"]
			tDisk+= i["attributes"]["limits"]["disk"]
	return (True, uDt, tCPU, tDisk, tRam)

def createPteroServer(name, user, node, egg, cpu, ram, disk):
	uDt = getUser(user)
	uPdt = checkPteroUser(user)
	uSv = listPteroServer(user)

	if (uDt[0] == False) or (uPdt[0] == False):
		return (False, "User not found.", {
			"uDt": uDt,
			"uPdt": uPdt
		})
	eggs = config["eggs"]
	if (egg not in list(eggs.keys())):
		return (False, "Egg not found.")
	egg = config["eggs"][egg]
	
	if node not in list(config["locations"].keys()):
		return (False, "Node not found.")
	
	ucpu = uDt[1]["cpu"]-uSv[2] #pyright: ignore
	udisk = uDt[1]["disk"]-uSv[3] #pyright: ignore
	uram = uDt[1]["ram"]-uSv[4] #pyright: ignore

	if (ucpu < cpu):
		return (False, "Not enough cpu.")
	elif (udisk < disk):
		return (False, "Not enough disk.")
	elif (uram < ram):
		return (False, "Not enough ram.")
	elif len(uSv[1]) >= uDt[1]["slot"]:
		return (False, "Not enough slot.")
	
	data = egg["info"]
	e = getPteroAllocation(node)
	if not e[0]: #pyright:ignore
		return (False, "No allocation available.")
	data["name"]=name
	data["user"]=uPdt[1]["id"]
	data["allocation"] = {
			"default": e[1]["id"] #pyright:ignore
		}
	data["limits"] = {
			"memory": ram,
			"swap": 0,
			"disk": disk,
			"io": 500,
			"cpu": cpu
		}

	resp = requests.post(pteroHost+"/api/application/servers", json=data, headers=headers).json()
	if (resp.get("errors")): return (False, resp["errors"][0])
	return (True, resp)

def delPteroServer(id):
	resp = requests.delete(pteroHost+f"/api/application/servers/{id}", headers=headers)
	if (resp.status_code!=204): return (False, resp.json()["errors"][0])
	return (True,)

def chMX(domain):
	try:
		r = dns.resolver.resolve(domain, "MX")
	except Exception:
		return 0
	else: return len(r)


def getPteroPasswd(e):
	passwd = "".join(random.choice(_chr) for i in range(20))
	data = {
			"email": e[1]["email"],
			"username": e[1]["username"],
			"first_name": e[1]["first_name"],
			"last_name": e[1]["last_name"],
			"password": passwd
		}
	try: resp = requests.patch(pteroHost+f"/api/application/users/{e[1]['id']}",json=data, headers=headers)
	except Exception:
		return (False, "Something went wrong!")
	else:
		return (True, passwd)

def editPteroServer(user, identifier, cpu, ram, disk):
	uDt = getUser(user)
	uSv = listPteroServer(user)
	for i in uSv[1]:
		if i["identifier"] == identifier: #pyright:ignore
			if i["status"] == "suspended": #pyright:ignore
				return (False,"This server has been suspended.")
			
			ucpu = uDt[1]["cpu"]-uSv[2] #pyright: ignore
			udisk = uDt[1]["disk"]-uSv[3] #pyright: ignore
			uram = uDt[1]["ram"]-uSv[4] #pyright: ignore
			ccpu = i["limits"]["cpu"] #pyright: ignore
			cdisk = i["limits"]["disk"] #pyright: ignore
			cram = i["limits"]["memory"] #pyright: ignore

			if (ucpu < (cpu - ccpu)):
				return (False, "Not enough cpu.")
			elif (udisk < (disk - cdisk)):
				return (False, "Not enough disk.")
			elif (uram < (ram - cram)):
				return (False, "Not enough ram.")

			data = {
				"allocation": i["allocation"], #pyright: ignore
				"memory": ram,
				"swap": i["limits"]["swap"], #pyright: ignore
				"disk": disk,
				"io": i["limits"]["io"], #pyright: ignore
				"cpu": cpu,
				"feature_limits": i["feature_limits"] #pyright: ignore
			}

			resp = requests.patch(pteroHost+f"/api/application/servers/{i['id']}/build", json=data, headers=headers).json() #pyright: ignore
			if (resp.get("errors")): return (False, resp["errors"][0])
			return (True, resp)
	return (False,"You don't have permission to modify this server.")