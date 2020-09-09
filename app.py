#!/usr/bin/env python

from flask import Flask
from flask_restful import Api

from resources import EmployeeListResource
from resources import EmployeeResource

app = Flask(__name__)
api = Api(app)


api.add_resource(EmployeeListResource, '/employees/', endpoint='employees')
api.add_resource(EmployeeResource, '/employees/<string:name>/', endpoint='employee')

if __name__ == '__main__':
    app.run(debug=True)
