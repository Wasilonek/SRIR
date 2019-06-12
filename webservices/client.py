#!flask/bin/python3
import socket
import requests, json, time
from flask import Flask, Response, request
from multiprocessing import Process

app = Flask(__name__)
#SERVER_ENDPOINT = 'http://192.168.191.117:5000/postjson'
SERVER_ENDPOINT = 'http://192.168.43.180:5000/postjson'


@app.route('/info', methods=['POST'])
def post():
    content = json.loads(request.data)
    information = content["message"]
    for info in information:
        print(info)
    return Response(
        mimetype='application/json',
        status=200
    )


def send_request(file_name):
    """

    :param file_name: comment
    """
    with open(file_name, "r") as file_object:
        program_code = file_object.read()

    IP = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1],
                       [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    data = {
        "kod_programu": program_code,
        "IP": IP
    }
    requests.post(url=SERVER_ENDPOINT, data=json.dumps(data))


if __name__ == '__main__':
    info_receiver = Process(target=app.run, kwargs={"host": '0.0.0.0', "port": 5001})
    info_receiver.start()

    while True:
        time.sleep(1)
        print("\nPodaj nazwe pliku: ")
        file_name = input()
        if file_name == "exit()":
            break
        code_sender = Process(target=send_request, args=[file_name])
        code_sender.start()
        code_sender.join()

    info_receiver.terminate()
    info_receiver.join()
