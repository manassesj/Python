from flask import request
from flask_mysqldb import MySQL
from flask_restful import Resource
from config import app, api, mysql

# app = Flask(__name__)
# api = Api(app)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'test'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS `chat` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(32) NOT NULL,
    PRIMARY KEY (`id`)
)''')
    return 'sucess'


@app.route('/insert', methods=['POST'])
def insert():
    name = request.json['name']
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO `chat`(`username`) VALUES (%s)''', [name])

    cur.execute('''SELECT * FROM `chat` 
                        ORDER BY id DESC
                        LIMIT 1''')
    user = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return user


# @app.route('/getAll', methods=['GET'])
# def getAll():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT * FROM `chat`''')

#     users = {}

#     allUsers = cur.fetchall() 
#     print(allUsers)

#     if len(allUsers) > 0:
#         for user in allUsers:
#             body = {}
#             id = user['id']
#             body['username'] = user['username']
#             users[id] = body
#         return users
#         mysql.connection.commit()
#         cur.close()
#     else:
#         mysql.connection.commit()
#         cur.close()
#         return 'Errorrr' 

class getAll(Resource):
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM `chat`''')

        users = {}

        allUsers = cur.fetchall() 
        print(allUsers)
        if len(allUsers) > 0:
            for user in allUsers:
                body = {}
                id = user['id']
                body['username'] = user['username']
                users[id] = body
            return users
            mysql.connection.commit()
            cur.close()
        else:
            mysql.connection.commit()
            cur.close()
            return 'Error'

api.add_resource(getAll, '/getAll')

if __name__ == '__main__':
    #.run(debug=True)
    app.run(host='0.0.0.0')