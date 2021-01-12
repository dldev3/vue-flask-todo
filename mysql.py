from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'vue_flask_todo'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
CORS(app)

@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM vue_flask_todo.tasks")
    rv = cur.fetchall()
    return jsonify(rv)

@app.route('/api/task', methods=['POST'])
def add_task():
    cur = mysql.connection.cursor();
    task = request.get_json()['task']
    cur.execute("INSERT INTO vue_flask_todo.tasks (task) VALUES ('"+ str(task) +"') ")
    mysql.connection.commit()
    result = {'task' : task}
    return jsonify({'result': result})
    
@app.route('/api/task/<id>', methods=['PUT'])
def update_task(id):
    cur = mysql.connection.cursor()
    task = request.get_json()['task']
    cur.execute("UPDATE vue_flask_todo.tasks SET task = '"+ str(task)  +"' WHERE id = " + id)
    mysql.connection.commit()
    result = {'task':task}
    return jsonify({'result': result})

@app.route('/api/task/<id>',methods=['DELETE'])
def delete_task(id):
    cur = mysql.connection.cursor()
    response = cur.execute("DELETE FROM vue_flask_todo.tasks WHERE id ="+id)
    mysql.connection.commit()
    
    if response > 0 :
        result = { 'message': 'record deleted'}
    else:
        result = {'message': 'no record found'}
    
    return jsonify({'result': result})
    
    
if __name__ == '__main__':
    app.run(debug=True)
