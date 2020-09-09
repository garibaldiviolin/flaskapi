from models import Employee
from db import session

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

employee_fields = {
    'id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'deleted_at': fields.DateTime,
    'name': fields.String,
    'city': fields.String,
    'age': fields.Integer,
    'status': fields.Boolean
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('city', type=str)
parser.add_argument('age', type=int)
parser.add_argument('status', type=bool)


class EmployeeResource(Resource):
    @marshal_with(employee_fields)
    def get(self, name):
        employee = session.query(Employee).filter(Employee.name == name).first()
        if not employee:
            abort(404, message="Employee {} doesn't exist".format(name))
        return employee

    def delete(self, name):
        employee = session.query(Employee).filter(Employee.name == name).first()
        if not employee:
            abort(404, message="Employee {} doesn't exist".format(name))
        session.delete(employee)
        session.commit()
        return {}, 204

    @marshal_with(employee_fields)
    def patch(self, name):
        parsed_args = parser.parse_args()
        employee = session.query(Employee).filter(Employee.name == name).first()
        # employee.name = parsed_args['name']
        employee.city = parsed_args['city']
        employee.age = parsed_args['age']
        session.add(employee)
        session.commit()
        return employee, 200


class EmployeeListResource(Resource):
    @marshal_with(employee_fields)
    def get(self):
        employees = session.query(Employee).all()
        return employees

    @marshal_with(employee_fields)
    def post(self):
        parsed_args = parser.parse_args()
        employee = Employee(
            name=parsed_args['name'],
            city=parsed_args['city'],
            age=parsed_args['age'],
            status=parsed_args['status'],
        )
        session.add(employee)
        session.commit()
        return employee, 201
