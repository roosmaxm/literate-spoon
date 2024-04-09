import os, psycopg
from psycopg.rows import dict_row
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv 

# pip install psycopg_binary python-dotenv

load_dotenv()

PORT=8300 

db_url = os.environ.get("DB_URL")
print(os.environ.get("FOO"))

conn = psycopg.connect(db_url, row_factory=dict_row)

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

roomsTEMP = [
    { 'number': 101, 'type': "single" },
    { 'number': 202, 'type': "double" },
    { 'number': 303, 'type': "suite" }
]

@app.route("/", )
def info():
    #return "<h1>Hello, Flask!</h1>"
    return "Hotel API, endpoints /rooms, /bookings"


@app.route("/rooms", methods=['GET', 'POST'])
def rooms_endoint():
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        roomsTEMP.append(request_body)
        return { 
            'msg': f"Du har skapat ett nytt rum, id: {len(roomsTEMP)-1}!"
        }
    else:
        with conn.cursor() as cur:
            cur.execute("""SELECT * 
                        FROM hotel_room 
                        ORDER BY room_number""")
            return cur.fetchall()

@app.route("/rooms/<int:id>", methods=['GET', 'PUT', 'PATCH', 'DELETE'] )
def one_room_endpoint(id):
        if request.method == 'GET':
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * 
                    FROM hotel_room 
                    WHERE id = %s""", [id])

                return cur.fetchone()
        
@app.route("/bookings", methods=['GET', 'POST'])
def bookings():
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        # Skapa rad i hotel_booking med sql INSERT INTO...
        return { 
            "msg": "APIN svarar!", 
            "request_body": request_body 
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))