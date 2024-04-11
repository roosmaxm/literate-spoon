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

conn = psycopg.connect(db_url, autocommit=True, row_factory=dict_row)

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


@app.route("/guests", methods=['GET'])
def guests_endoint():
    with conn.cursor() as cur:
        cur.execute("""SELECT 
                            hotel_guest.*, 
                            (
                                SELECT COUNT(*) 
                                FROM hotel_booking 
                                WHERE hotel_booking.guest_id = hotel_guest.id
                            ) AS previous_visits 
                        FROM 
                            hotel_guest 
                        ORDER BY 
                            hotel_guest.firstname""")
        return cur.fetchall()



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
    if request.method == 'GET':
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    hotel_booking.datefrom, 
                    hotel_booking.room_id, 
                    hotel_booking.guest_id, 
                    hotel_guest.firstname AS guest_name, 
                    hotel_room.room_number
                FROM 
                    hotel_booking
                INNER JOIN 
                    hotel_guest ON hotel_booking.guest_id = hotel_guest.id
                INNER JOIN 
                    hotel_room ON hotel_booking.room_id = hotel_room.id
                ORDER BY 
                    hotel_booking.datefrom
            """)
            return cur.fetchall()
        
    if request.method == 'POST':
        body = request.get_json()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO hotel_booking (
                    room_id, 
                    guest_id,
                    datefrom
                ) VALUES (
                    %s, 
                    %s, 
                    %s
                ) RETURNING id""", [ 
                body['room'], 
                body['guest'], 
                body['datefrom'] 
            ])
            result = cur.fetchone()
    
        return { "msg": "Du har bokat ett rum!", "result": result }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))