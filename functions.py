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


def get_submenus(cnx, organization_id):
    cursor = cnx.cursor()
    cursor.execute(f"SELECT s.ID, s.submenu_name\
                FROM sub_menu AS s \
                INNER JOIN menu AS m \
                ON s.menu_id = m.ID \
                WHERE m.Organization_id = {organization_id}")
    submenus = [{
        'submenu_id': i[0],
        'submenu_name': i[1],
        'items': []} for i in cursor]

    submenu_cnt = len(submenus)
    
    for i in submenus:
        cursor.execute(
            f"SELECT * FROM food WHERE Submenu_id = {i['submenu_id']}")
        item = [{
            'id': j[0],
            'price': j[1],
            'name': j[2],
            'description': j[6],
            'image': j[4],
            'weight': j[5]} for j in cursor]
        i['items'] = item
        i['items_count'] = len(item)

    return (submenus, submenu_cnt)


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
