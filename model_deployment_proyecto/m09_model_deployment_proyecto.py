#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/python

from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
from m09_model_deployment_proyecto1 import predict_price
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

api = Api(
    app, 
    version='1.0', 
    title='Price Car Prediction API',
    description='Price Car Prediction API')

ns = api.namespace('predict', 
     description='Price Car Regressor')
   
parser = api.parser()

parser.add_argument(
    'YEAR', 
    type=int, 
    required=True, 
    help='Year of the car', 
    location='args')

parser.add_argument(
    'STATE', 
    type=str, 
    required=True, 
    help='state where the car was sold', 
    location='args')

parser.add_argument(
    'MAKE', 
    type=str, 
    required=True, 
    help='make of the car', 
    location='args')

parser.add_argument(
    'MODEL', 
    type=str, 
    required=True, 
    help='Model of the car', 
    location='args')

parser.add_argument(
    'MILEAGE', 
    type=int, 
    required=True, 
    help='Mileage of the car', 
    location='args')

resource_fields = api.model('Resource', {
    'result': fields.String,
})

@ns.route('/')
class PriceApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        
        return {
         "result": predict_price(args['YEAR','STATE','MAKE','MODEL','MILEAGE'])
        }, 200
    
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

