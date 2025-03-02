import bcrypt

def encode(passwd):
    bytes = passwd.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt) 
    return hash

def checkpw(hpw:bytes, pw):
    enpw = pw.encode('utf-8') 
    return bcrypt.checkpw(enpw, hpw)