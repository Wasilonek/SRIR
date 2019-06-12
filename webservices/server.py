#!flask/bin/python3
from contextlib import redirect_stdout
import json, requests, ast, threading, io, difflib
from flask import request, Response
from webservices.models import Result
from webservices import app, db


@app.route('/postjson', methods=['POST'])
def post():
    content = json.loads(request.data)
    thr = threading.Thread(target=async_task, args=[content], kwargs={})
    thr.start()
    return Response(
        mimetype='application/json',
        status=200
    )


def async_task(content):
    IP = content["IP"]
    CLIENT_ENDPOINT = "http://" + IP + ":5001/info"
    program_code = content["kod_programu"]
    data = syntax_check(program_code)
    requests.post(CLIENT_ENDPOINT, data=json.dumps(data))
   


def syntax_check(program_code):
    try:
        ast.parse(program_code)
        result = "1. Poprawna skladnia"
    except SyntaxError:
        result = "1. Niepoprawna skladnia"
    data = {
        "message": [result]
    }
    return data


