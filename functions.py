def get_users(cnx):
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users")
    res = [{
        'ID': i[0],
        'Email': i[1],
        'Name': i[2],
        'Surname': i[3],
        'Password': i[4],
        'Phone_number': i[5]} for i in cursor]

    return res


def get_user_by_id(cnx, id):
    cursor = cnx.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = '{id}'")
    res = [{
        'ID': i[0],
        'Email': i[1],
        'Name': i[2],
        'Surname': i[3],
        'Password': i[4],
        'Phone_number': i[5]} for i in cursor]

    return res


def get_user_by_email(cnx, email):
    cursor = cnx.cursor()
    cursor.execute(f"SELECT * FROM users WHERE Email = '{email}'")
    res = [{
        'ID': i[0],
        'Email': i[1],
        'Name': i[2],
        'Surname': i[3],
        'Password': i[4],
        'Phone_number': i[5]} for i in cursor]

    return res


def insert_user(cnx, email, password, name, surname, phone_number):
    cursor = cnx.cursor()
    cursor.execute(f"INSERT INTO users (Email, Passwords, Name, Surname, Phone_number) VALUES (\
                        '{email}',\
                        '{password}',\
                        '{name}',\
                        '{surname}',\
                        '{phone_number}')")
    cnx.commit()


def is_email_exists(cnx, email):
    cursor = cnx.cursor(buffered=True)
    cursor.execute(f"SELECT * FROM users WHERE Email = '{email}'")

    return cursor.rowcount == 1
