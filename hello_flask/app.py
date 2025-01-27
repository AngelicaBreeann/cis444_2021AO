from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt


from db_con import get_db_instance, get_db

app = Flask(__name__, template_folder = "templates")
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/class') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-9' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))

    return render_template('backatu.html',input_from_browser= str(request.form) )
@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)




#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")

#Assigment 3
@app.route('/loginStore',  methods=['GET']) #endpoint
def userLogin():
    return render_template('BookPage.html')

@app.route('/loginPage',  methods=['POST']) #endpoint
def loginUser():
    userInput = request.form['username']
    pwInput =  request.form['password']
    cur = global_db_con.cursor()
    cur.execute(f"select * from users where username = '{userInput}';")
    data = cur.fetchone()

    if data is None:
        print('data is null')
    else:
        print('here')    

    salted = bcrypt.hashpw( bytes(request.form['password'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)
    cur.execute(f"select password from users where username = '{userInput}';")
    correctInput = cur.fetchone()[0]
    correctInput = bytes(correctInput, 'utf-8')
    if( bcrypt.checkpw( bytes(request.form['password'], 'utf-8') , correctInput)):
        print("testing:")
        print(pwInput)
        print (correctInput)
    else:
        print("INVALID")

@app.route('/textTable',  methods=['POST']) #endpoint
def addTable():
    book_name = request.form['bookname_']
    secret = 'secret'
    cur = g.db.cursor()
    cur.execute(f"INSERT INTO book(bookname) VALUES('{book_name}');")
    g.db.commit()
    logger.debug("User input added")
    chat_list= []
    dataBook = { "input" : bookname}
    chat_list.append(dataBook)
    jwt_str = jwt.encode(dataBook,secret,algoritm="HS256")
    return jsonify({'data':dataBook, 'message':'Message Recieved', 'token':jwt_str})


    
   #words = request.form['bookname']
    #cur.execute(f"select password from users where username = '{userInput}';")
    # cursor.execute("INSERT INTO book(bookname) VALUES (%s)",(bookname))
  # cur.execute(f"INSERT INTO book(bookname) VALUES (%s)",(bookname))
   #conn.commit()
   #print("TESTING!!!!!!")
  # print (bookname)



    
#GET 6
#app.route('/bookStore', methods=['GET'])
#def buybook():
   # booktitle = request.args.get("bookname")
    #return render_template{'bookPage.html'}






app.run(host='0.0.0.0', port=80)

