from flask import Flask
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from modelo.model import redirection

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins
acortador = redirection ()

api = Api(
    app, 
    version='1.0', 
    title='Redireccionar URL',
    description='Redireccionador de URL segun URL acortada')

ns = api.namespace('Redireccionar')
   
parser = api.parser()

parser.add_argument(
    'url', 
    type=str, 
    required=True, 
    help='Url Acortada', 
    location='args')

resource_fields = api.model('Resource', {
    'result': fields.String,
})

@ns.route('/Short')
class Acortar(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()

        return {
         "result":acortador.redireccionar_url(args['url'])
        }, 200
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)