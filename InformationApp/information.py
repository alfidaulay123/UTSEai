from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pariwisata_informasi'

mysql = MySQL(app)

def generate_response(status_code, message, data=None):
    response = {'status_code': status_code, 'message': message, 'timestamp': datetime.now().isoformat()}
    if data:
        response['data'] = data
    return jsonify(response), status_code

@app.route('/')
def root():
    return 'Selamat datang di web pariwisata'

@app.route('/detailinformasi', methods=['GET'])
def detailinformasi():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM information WHERE product_id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)

        #get column names from cursor.decription
        column_names = [i[0] for i in cursor.description]

        #fetch data and format into list of dictionaries
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
            
        return jsonify(data)
        cursor.close()

@app.route('/addinformasi', methods=['POST'])
def addinformasi():
    data = request.get_json()
    name = data['name']
    description = data['description']
    location = data['location']

    cursor = mysql.connection.cursor()
    sql = "INSERT INTO information (name, description, location) VALUES (%s, %s, %s)"
    val = (name, description, location)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

    return generate_response(201, 'Information added successfully')


@app.route('/updateinformasi', methods=['PUT'])
def updateinformasi():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE informion SET name=%s, description=%s, location=%s WHERE product_id=%s"
        val = (data['name'], data['description'], data['location'], request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()

        return jsonify({'message': 'Information updated successfully'})
    else:
        return jsonify({"error": "Prouct tidak ditemukan"}), 404
    cursor.close()

    
@app.route('/deleteinformasi', methods=['DELETE'])
def deleteinformasi():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM information WHERE product_id=%s"
        val = (request.args['id'],)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return generate_response(200, 'Product deleted successfully')
    else:
        return generate_response(400, 'Could not delete Product')


if __name__ == '__main__':
    app.run(debug=True, port=5003)