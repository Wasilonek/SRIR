#!flask/bin/python3
from contextlib import redirect_stdout
import json, requests, ast, threading, io, difflib
from flask import request, Response
from webservices.models import Result
from webservices import app, db

#   Description: Send information to client
#
#   Parameters: none
#
#   Return value: none
#
@app.route('/postjson', methods=['POST'])
def post():
    content = json.loads(request.data)
    thr = threading.Thread(target=async_task, args=[content], kwargs={})
    thr.start()
    return Response(
        mimetype='application/json',
        status=200
    )


#   Description: Send request to client and save it in database
#
#   Parameters: content - request content from client
#
#   Return value: none
#
def async_task(content):
    IP = content["IP"]
    CLIENT_ENDPOINT = "http://" + IP + ":5001/info"
    # 2
    program_code = content["kod_programu"]
    data = syntax_check(program_code)
    requests.post(CLIENT_ENDPOINT, data=json.dumps(data))
    # 3
    if data.get("message") == ["1. Poprawna skladnia"]:
        data, execution_result = compile_program(program_code)
        requests.post(CLIENT_ENDPOINT, data=json.dumps(data))
        # 4
        programs = Result.query.all()
        data = check_difference(programs, program_code)
        requests.post(CLIENT_ENDPOINT, data=json.dumps(data))
        result = Result(program_result=execution_result,
                        program_code=program_code)
        db.session.add(result)
        db.session.commit()


#   Description: Check syntax of program code
#
#   Parameters: program_code - program code
#
#   Return value: Callback
#
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


#   Description: Compile program, which was sand from client
#
#   Parameters: program_code - program code
#
#   Return value: Callback
#
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


#   Description: Check differences between program sand by client with programs in data base
#
#   Parameters: programs - table of Result objects
#               program_code - program code
#
#   Return value: Callback
#
def check_difference(programs, program_code):
    differ = difflib.Differ()
    differences = ["3. Porownanie z poprzednimi programami:"]
    for program in programs:
        diff = differ.compare(program.program_code, program_code)
        all_lines = transpose_diff(diff)
        differences.append("Diff Program: " + str(program.id))
        differences.append(all_lines)
    data = {
        "message": differences
    }
    return data


#   Description: Convert data from check_difference to readable version to client
#
#   Parameters: diff - data
#
#   Return value: Readable version
#
def transpose_diff(diff):
    first_line = ""
    second_line = ""
    all_lines = ""
    checker = ''
    for d in diff:
        checker = d[2]
        first_line += d[2]
        if d[2] != "\n":
            second_line += d[0]
        else:
            all_lines += first_line + second_line + "\n"
            first_line = ""
            second_line = ""
    if checker != "\n":
        first_line += "\n"
    all_lines += first_line + second_line + "\n"
    return all_lines
