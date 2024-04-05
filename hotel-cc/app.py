import os, psycopg
from psycopg.rows import dict_row
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

PORT=8300 

db_url = os.environ.get("DB_URL")
print(db_url)

conn = psycopg.connect(db_url, autocommit=True, row_factory=dict_row)

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

rooms = [
    { 'number': 101, 'type': "single" },
    { 'number': 202, 'type': "double" },
    { 'number': 303, 'type': "suite" }
]

@app.route("/test", )
def dbtest():
     with conn.cursor() as cur:
        cur.execute("SELECT * from people")
        rows = cur.fetchall()
        return rows
    

@app.route("/rooms", methods=['GET', 'POST'])
def rooms_endoint():
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        rooms.append(request_body)
        return { 
            'msg': f"Du har skapat ett nytt rum, id: {len(rooms)-1}!"
        }
    else:
        return rooms

@app.route("/rooms/<int:id>", methods=['GET', 'PUT', 'PATCH', 'DELETE'] )
def one_room_endpoint(id):
        if request.method == 'GET':
            return rooms[id]
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))