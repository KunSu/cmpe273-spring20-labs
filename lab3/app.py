from ariadne import ObjectType, QueryType, MutationType, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

app = Flask(__name__)

STUDENT_ID = 1
CLASS_ID = 1
STUDENT_MAP = {}
CLASS_MAP = {}

type_defs = """
    type Query {
        students(id: Int!): Student
        classes(id: Int!): Class
    }

    type Student {
        id: ID!
        name: String!
    }

    type Class {
        id: ID!
        name: String!
        students: [Student!]!
    }

    type Mutation {
        addStudent(name: String!): Student
        addClass(name: String!): Class
        addStudentIntoClass(classID: Int!, studentID: Int!): Class
    }
    
"""

query = QueryType()
mutation = MutationType()

@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

@query.field("students")
def resolve_students(*_, id):
    if (id in STUDENT_MAP):
        return STUDENT_MAP[id]

@query.field("classes")
def resolve_classes(*_, id):
    if (id in CLASS_MAP):
        return CLASS_MAP[id]

@mutation.field("addStudent")
def resolve_addStudent(*_, name):
    global STUDENT_ID

    studentID = STUDENT_ID
    STUDENT_MAP[studentID] = {
        'id' : studentID,
        'name'  : name
    }
    STUDENT_ID += 1

    return STUDENT_MAP[studentID]

@mutation.field("addClass")
def resolve_addClass(*_, name):
    global CLASS_ID

    classID = CLASS_ID
    CLASS_MAP[classID] = {
        "id" : classID,
        "name" : name,
        "students" : []
    }
    CLASS_ID += 1

    return CLASS_MAP[classID]

@mutation.field("addStudentIntoClass")
def addStudentIntoClass(*_, classID, studentID):

    if classID in CLASS_MAP and studentID in STUDENT_MAP:

        # add student into student list (duplicate allowed)
        CLASS_MAP[classID]['students'].append(STUDENT_MAP[studentID])
        return CLASS_MAP[classID]

schema = make_executable_schema(type_defs, [query, mutation])
