from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger
import bcrypt
def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    cur = g.db.cursor()
    userInput = request.form['firstname']
    password_from_user_form = request.form['password']
    user = {
            "sub" : request.form['firstname'] #sub is used by pyJwt as the owner of the token
            }
    if not user:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

    cur.execute(f"select password from users where username = '{userInput}';")
    correctInput = cur.fetchone()[0]
    correctInput = bytes(correctInput, 'utf-8')
    if( bcrypt.checkpw( bytes(request.form['password'], 'utf-8') , correctInput)):
        return json_response( token = create_token(user) , authenticated = True)
    else:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )



def addtoTable():
   words = request.form['bookname']
   cur.execute(f"INSERT INTO book(bookname) VALUES (%s)",(bookname))
   conn.commit()
   print("TESTING!!!!!!")
   print (bookname)
