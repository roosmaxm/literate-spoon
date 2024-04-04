from flask import Flask, request
from flask_cors import CORS 

PORT = 8300

app = Flask(__name__)
CORS(app)  # Tillåt cross-origin requests

@app.route("/", methods=['GET', 'POST'])
def hello():
    user_ip = request.remote_addr
    return {
        "ip": user_ip,
    'method': request.method
    }

@app.route("/test", methods=['GET', 'POST'])
def test():{
    'msg': "TESTING!",
    "method": request.method
}

@app.route("/test/<int:id>", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def testId(id):
    if request.method == 'GET':
       return{
        'msg': f"Här får du id: {id}",
        'method': request.method
    }

    if request.methdod == 'PUT':
            return{
        'msg': f"Du uppdaterar id: {id}",
        'method': request.method
        }

    if request.methdod == 'DELETE':
            return{
        'msg': f"Du har raderat: {id}",
        'method': request.method
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))
