import bcrypt
import hashlib

def hash(inp):
<<<<<<< HEAD
    if (not inp): inp=""
    input_bytes = inp.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_bytes)
    hashed_string = sha256_hash.hexdigest()
    return hashed_string
=======
	if inp == None: inp=""
	input_bytes = inp.encode('utf-8')
	sha256_hash = hashlib.sha256()
	sha256_hash.update(input_bytes)
	hashed_string = sha256_hash.hexdigest()
	return hashed_string
>>>>>>> 61c988cc4f6ec69c2e602301988ed27d607fd054

def encode(passwd):
	bytes = passwd.encode('utf-8')
	salt = bcrypt.gensalt()
	hash = bcrypt.hashpw(bytes, salt) 
	return hash

def checkpw(hpw:bytes, pw):
	enpw = pw.encode('utf-8') 
	return bcrypt.checkpw(enpw, hpw)
