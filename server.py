from flask import Flask, request, jsonify
from mysql.connector import (connection)

config = {
  'user': 'onlineord',
  'password': 'Bd4tO--2FL7V',
  'host': 'den1.mysql4.gear.host',
  'database': 'onlineord',
  'raise_on_warnings': True
}

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/users/', methods=['GET'])
def user():
    cnx = connection.MySQLConnection(**config)
    id = request.args.get('id', None)
    
    if id:
        cursor = cnx.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = '{id}'")

        response = [{
            'ID': i[0],
            'Email': i[1],
            'Name': i[2],
            'Surame': i[3],
            'Password': i[4],
            'Phone_number': i[5]} for i in cursor]
    else:
        cursor = cnx.cursor()
        cursor.execute(f"SELECT * FROM users")

        response = [{
            'ID': i[0],
            'Email': i[1],
            'Name': i[2],
            'Surame': i[3],
            'Password': i[4],
            'Phone_number': i[5]} for i in cursor]

    cnx.close()
    return jsonify(response)

@app.route('/users/', methods=['POST'])
def login():
    cnx = connection.MySQLConnection(**config)
    
    req_email = request.form['email']
    req_pass = request.form['password']
    
    cursor = cnx.cursor(buffered=True)
    cursor.execute(f"SELECT * FROM users WHERE Email = '{req_email}'")

    if(cursor.rowcount == 1):
        user = [{
            'ID': i[0],
            'Email': i[1],
            'Name': i[2],
            'Surame': i[3],
            'Password': i[4],
            'Phone_number': i[5]} for i in cursor]
        
        if(user[0]['Password'] == req_pass):
            response = user
        else:
            response = [{
            'error': {
                'code': 1,
                'description': "invalid password"
            }
        }]
    else:
        response = [{
            'error': {
                'code': 0,
                'description': "invalid email"
            }
        }]

    cnx.close()
    return jsonify(response)

@app.route("/")
def home():
    return "OnlineOrders server works!"

if __name__ == "__main__":
    app.run(threaded=True, port=5000)