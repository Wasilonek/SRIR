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
	if data.get("message") == ["1. Poprawna skladnia"]:
		data, execution_result = compile_program(program_code)
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
	

def compile_program(program_code):
    compiled_object = compile(program_code, 'program', 'exec')
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            exec(compiled_object)
        execution_result = f.getvalue()
        result = "2. Program wykonano poprawnie z wynikiem:\n" + execution_result
    except Exception as e:
        execution_result = str(e)
        result = "2. Program wykonany z bledami:\n" + execution_result
    data = {
        "message": [result]
    }
    return data, execution_result

