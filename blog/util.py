#Checks regular expressions
import re
#Escapes inpout
import cgi
#Hashed Passwords
import hashlib
#Creates a salt
import random
#Hashes the cookie
import hmac

#Creates the hash
from string import letters
#Import the User Database
from models import User

# Excpetion for objects that don't exist in the database
from django.core.exceptions import ObjectDoesNotExist

import secret

secret = secret.SECRET

#Regular Expresions for input
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile("^.{3,20}$")
EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")


#Matches the user input with the regular expressions
def checkUsername(user):
	return USER_RE.match(user)

def checkPass(password):
	return PASS_RE.match(password)

def checkEmail(email):
	return not email or EMAIL_RE.match(email)


#Compares two passwords
def comparePassword(password, verify):
	if(password == verify):
		return True
	return False

#Escapes html, or other input
def escape(s):
	return cgi.escape(s, quote=True)

#Creates a salt for the password
def make_salt(length = 5):
	return ''.join(random.choice(letters) for x in xrange(length))

#Hashes the passwords using the name, password and a salt if one already exists
def make_pw_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s|%s' % (salt, h)

#Checks if a password matches a hash
def valid_pw(name, password, h):
	salt = h.split('|')[0]
	return h == make_pw_hash(name, password, salt)

#Checks the user cookie to see if a user is logged in
#and if there cookie is valid
def checkLoggedIn(request):
	username = None
	error = ""
	if request.COOKIES.has_key( 'user' ):
		if check_secure_val(request.COOKIES['user']):
			uid = request.COOKIES[ 'user' ].split('|')[0]
			try:
				user =  User.objects.get(pk=uid)
			except ObjectDoesNotExist:
				return None
			if user:
				return user
			else:
				return None
		else:
			return None

#Creates a secure cookie
def make_secure_val(val):
  	return '%s|%s' % (val, hmac.new(secret, val).hexdigest())
  
 #Checks if a value was created with the make_secure_val function
def check_secure_val(secure_val):
  	val = secure_val.split('|')[0]
  	if secure_val == make_secure_val(val):
  	  return val
  	  
def log_traceback(exception, args):
    import sys, traceback, logging
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    logging.debug(exception)
    logging.debug(args)
    for tb in traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback):
        logging.debug(tb)
	
