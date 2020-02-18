from flask import Flask, escape, request
import json

app = Flask(__name__)

STUDENT_ID = 1
CLASS_ID = 1
STUDENT_MAP = {}
CLASS_MAP = {}

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/students', methods=['POST'])
def createStudent():
    global STUDENT_ID
    if request.method == 'POST':

        # get student name
        name = request.json['name']

        studentID = STUDENT_ID
        STUDENT_MAP[studentID] = {
            'id' : studentID,
            'name'  : name
        }
        STUDENT_ID += 1

        return json.dumps(STUDENT_MAP[studentID]), 201

@app.route('/students/<int:id>', methods=['GET'])
def getStudent(id):
    if request.method == 'GET':
        if (id in STUDENT_MAP):
            return json.dumps(STUDENT_MAP[id])

        return "Student not found"
        
@app.route('/classes', methods=['POST'])
def createClass():
    global CLASS_ID
    if request.method == 'POST':

        # get class name
        name = request.json['name']
        
        classID = CLASS_ID
        CLASS_MAP[classID] = {
            "id" : classID,
            "name" : name,
            "students" : []
        }
        CLASS_ID += 1

        return json.dumps(CLASS_MAP[classID]), 201

@app.route('/classes/<int:id>', methods=['GET'])
def getClass(id):
    if request.method == 'GET':
        if (id in CLASS_MAP):
            return json.dumps(CLASS_MAP[id])
            
        return "Class not found"

@app.route('/classes/<int:classID>', methods=['PATCH'])
def addStudentIntoClass(classID):
    if request.method == 'PATCH':

        if classID in CLASS_MAP:

            # get Student ID from payload
            studentID = request.json['student_id']

            if studentID in STUDENT_MAP:

                # add student into student list (duplicate allowed)
                CLASS_MAP[classID]['students'].append(STUDENT_MAP[studentID])
                return json.dumps(CLASS_MAP[classID])
            
            return "Student not found"
        
        return "Class not found"
