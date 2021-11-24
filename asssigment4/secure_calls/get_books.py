from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get Books Handle Request")
    cur = g.db.cursor()
    cur.execute("select * from book")
    bookInfo = []
    for i in cur.fetchall():
        print('Books: ',i)
        displayBooks = {"id": i[0], "bookname":i[1], "price":i[2]}
        bookInfo.append(displayBooks)
    return json_response( token = create_token(  g.jwt_data ) , bookInfo =bookInfo)

