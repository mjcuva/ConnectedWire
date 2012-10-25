# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

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
# Mobile user agents
reg_b = re.compile(r"android.+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|meego.+mobile|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)



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

# Checks if user is mobile
def checkMobile(request):
    request.mobile = False
    # If there is a user agent
    if request.META.has_key('HTTP_USER_AGENT'):
        #Checks the user agent agianst list of agents
        user_agent = request.META['HTTP_USER_AGENT']
        b = reg_b.search(user_agent)
        v = reg_v.search(user_agent[0:4])
        if b or v:
            return False #IMPORTANT -- CHANGED FOR STYLESHEET TESTING
        else:
            return False

	
