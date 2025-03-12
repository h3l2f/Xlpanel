import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template
import json

app = Flask(__name__, template_folder="templates")
with open("config.json","r") as f:
    config = json.load(f)


def sendVerify(rEml, code):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = config["mail"]["smtp"]["from"]
        msg['To'] = rEml
        msg['Subject'] = f"Here is your verify code: {code}"

        with app.app_context():
            ctn = render_template("email.html", name=config["name"], code=code)

        ctn = MIMEText(ctn, 'html')
        msg.attach(ctn)

        with smtplib.SMTP_SSL(config["mail"]["smtp"]["host"], config["mail"]["smtp"]["port"]) as server:
            server.login(config["mail"]["smtp"]["user"], config["mail"]["smtp"]["password"])
            server.sendmail(config["mail"]["smtp"]["from"], rEml, msg.as_string())
        return (True, )
    except Exception as e:
        return (False, e)

def sendrspwd(rEml, passwd):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = config["mail"]["smtp"]["from"]
        msg['To'] = rEml
        msg['Subject'] = f"Reset password - {config['name']}"

        with app.app_context():
            ctn = render_template("forgotPass.html", name=config["name"], passwd=passwd)

        ctn = MIMEText(ctn, 'html')
        msg.attach(ctn)

        with smtplib.SMTP_SSL(config["mail"]["smtp"]["host"], config["mail"]["smtp"]["port"]) as server:
            server.login(config["mail"]["smtp"]["user"], config["mail"]["smtp"]["password"])
            server.sendmail(config["mail"]["smtp"]["from"], rEml, msg.as_string())
        return (True, )
    except Exception as e:
        return (False, e)