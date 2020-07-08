from flask import request
from flask_mysqldb import MySQL
from config import app, api, mysql

@app.route('/')
def createDbs():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS `User` 
                        (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `email` varchar(100) NOT NULL,
                        `name` varchar(150) NOT NULL
                        `password` varchar(32) NOT NULL,
                        PRIMARY KEY (`id`)
                        )''')

        cursor.close() 
        return 'Sucess in create tables'
    except:
        return 'An except occurred'


@app.route('/user/insert', methods=['POST'])
def insert():
    data = request.get_json(force=True)
    
    email = data['email']
    name = data['name']
    password = data['password']
    print("Email: " + email)
    print("Passoword: " + password)
    cursor = mysql.connection.cursor()
    
    cursor.execute('''SELECT `email`
                    FROM `User`
                    WHERE email = %s''', [email])

    if len(cursor.fetchall()) < 1:
        cursor.execute('''INSERT INTO `User`(`email`, `name`, `password`,) VALUES (%s, %s)''', [email, name, password])

        cursor.execute('''SELECT * FROM `User` 
                        ORDER BY id DESC
                        LIMIT 1''')
        user = cursor.fetchone()
        mysql.connection.commit()
        cursor.close() 
        return user 
    else:
        cursor.close()
        return {}

@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    
    email = data['email']
    password = data['password']
    print("email: " + email)
    print("PASSWORD: " + password)

    cursor = mysql.connection.cursor()

    cursor.execute('''SELECT `id`, `email`
                    FROM `User`
                    WHERE email = %s''', [email])

    if len(cursor.fetchall()) > 0:
        cursor.execute('''SELECT `id`,`email`, `password`
                    FROM `User`
                    WHERE email = %s AND password = %s''', [email, password])
        user = cursor.fetchone()
        mysql.connection.commit()
        cursor.close() 
        return user
    else:
        cursor.close()
        return {"status": "ERROR"} 


if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True)
