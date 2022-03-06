# ==============================imports=================================

from flask import Flask, request, jsonify
import sqlite3

# ==============================constants=================================

DATABASE_PATH = '../DATABASE/BTC.db'

# ==============================functions=================================

def create_tables(conn):
    btcDB = """
        CREATE TABLE IF NOT EXISTS btcDB (
            hash TEXT,
            block INTEGER PRIMARY KEY,
            time TIMESTAMP,
            count INTEGER
        );
    """
    c = conn.cursor()
    c.execute(btcDB)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    if conn!=None:
        create_tables(conn)
    return conn

def get_latest_Block():
    conn = create_connection(DATABASE_PATH)
    c = conn.cursor()

    data=None
    latestBlockQuery = f"""
            SELECT MAX(block),MAX(count),MAX(time) FROM btcDB w
        """
    data = c.execute(latestBlockQuery).fetchall()
    packet={'blockNumber':data[0][0],'count':data[0][1],'timestamp':data[0][2]}
    response = jsonify(packet)
    response.headers.add('Access-Control-Allow-Origin', '*')
    conn.close()
    return response

def get_Number_of_Delta():
    conn = create_connection(DATABASE_PATH)
    c = conn.cursor()

    data=None
    latestBlockQuery = f"""
            SELECT MAX(count) FROM btcDB w
        """
    data = c.execute(latestBlockQuery).fetchall()
    packet={'count':data[0][0]}
    response = jsonify(packet)
    response.headers.add('Access-Control-Allow-Origin', '*')
    conn.close()
    return response

# ============================api endpoints==================================
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/postinfo', methods=['POST'])
def post_data():
    data = request.get_json()
    conn = create_connection(DATABASE_PATH)
    c = conn.cursor()

    insert_into_btcDB_query = f"""
        INSERT OR IGNORE INTO btcDB (hash, block, time, count) VALUES (?, ?, ?, ?);"""

    for row in data['data']:
        c.execute(insert_into_btcDB_query, row)

    conn.commit()
    conn.close()

    return jsonify({"status": "success", "status_code": 200})

@app.route('/getinfo', methods=['GET'])
def postbBlockInfo():
    return get_latest_Block()

@app.route('/getdelta', methods=['GET'])
def postbDeltaInfo():
    return get_Number_of_Delta()