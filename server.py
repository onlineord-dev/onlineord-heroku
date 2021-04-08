from flask import Flask, request, jsonify
from mysql.connector import (connection)

import functions as db

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
def users():
    cnx = connection.MySQLConnection(**config)
    response = db.get_users(cnx)

    return jsonify(response)


@app.route('/users/<int:user_id>', methods=['GET'])
def user(user_id):
    cnx = connection.MySQLConnection(**config)
    response = db.get_user_by_id(cnx, user_id)

    return jsonify(response)


@app.route('/users/', methods=['POST'])
def login():
    cnx = connection.MySQLConnection(**config)

    req = {
        'email': request.form['email'],
        'password': request.form['password']
    }

    if db.is_email_exists(cnx, req['email']):
        user = db.get_user_by_email(cnx, req['email'])

        if user[0]['Password'] == req['password']:
            response = user
        else:
            response = [{
                'error': {
                    'code': 1,
                    'description': "invalid password",
                    'form-params': req
                }
            }]
    else:
        response = [{
            'error': {
                'code': 0,
                'description': "invalid email",
                'form-params': req
            }
        }]

    cnx.close()
    return jsonify(response)


@app.route('/users/new', methods=['POST'])
def registration():
    cnx = connection.MySQLConnection(**config)

    req = {
        'email': request.form['email'],
        'password': request.form['password'],
        'name': request.form['name'],
        'surname': request.form['surname'],
        'phone_number': request.form['phone_number']
    }

    if not db.is_email_exists(cnx, req['email']):
        db.insert_user(cnx, req['email'], req['password'],
                       req['name'], req['surname'], req['phone_number'])
        response = db.get_user_by_email(cnx, req['email'])
    else:
        response = [{
            'error': {
                'code': 0,
                'description': "email already exists",
                'form-params': req
            }
        }]

    cnx.close()
    return jsonify(response)


@app.route('/menu', methods=['POST'])
def get_menu():
    cnx = connection.MySQLConnection(**config)

    req = {
        "organization_id": request.form['organization_id'],
        "table": request.form['table']
    }

    response = {
        "menu": [
            {
                "submenu_id": 0,
                "submenu_name": "Гарячі страви",
                "items": [
                    {
                        "id": 0,
                        "name": "Name",
                        "description": "Lorem ipsum dolor sit amet.",
                        "image": "image.jpg",
                        "price": 128
                    },
                    {
                        "id": 1,
                        "name": "Name",
                        "description": "Lorem ipsum dolor sit amet.",
                        "image": "image.jpg",
                        "price": 128
                    }
                ]
            },
            {
                "submenu_id": 1,
                "submenu_name": "Закуски",
                "items": [
                    {
                        "id": 2,
                        "name": "Name",
                        "description": "Lorem ipsum dolor sit amet.",
                        "image": "image.jpg",
                        "price": 128
                    },
                    {
                        "id": 3,
                        "name": "Name",
                        "description": "Lorem ipsum dolor sit amet.",
                        "image": "image.jpg",
                        "price": 128
                    }
                ]
            }
        ],
        "discounts": [
            {
                "id": 5,
                "name": "Name",
                "description": "Lorem ipsum dolor sit amet.",
                "image": "image.jpg",
                "price": 128
            },
            {
                "id": 6,
                "name": "Name",
                "description": "Lorem ipsum dolor sit amet.",
                "image": "image.jpg",
                "price": 128
            }
        ],
        "dish_of_the_day": {
            "id": 7,
            "name": "Name",
            "description": "Lorem ipsum dolor sit amet.",
            "image": "image.jpg",
            "price": 128
        },
        "dish_of_the_week": {
            "id": 7,
            "name": "Name",
            "description": "Lorem ipsum dolor sit amet.",
            "image": "image.jpg",
            "price": 128
        }
    }
    cnx.close()
    return response


@app.route("/")
def home():
    return "OnlineOrders server works!"


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
