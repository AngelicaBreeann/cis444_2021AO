from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

input_function():
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
