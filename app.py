from flask import Flask, redirect
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from modelo.model import AcortadorUrl

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins
acortador = AcortadorUrl ()

api = Api(
    app, 
    version='1.0', 
    title='Url Shortener',
    description='url shortener with pshishing detection')

ns = api.namespace('url')
   
parser = api.parser()

parser.add_argument(
    'url', 
    type=str, 
    required=True, 
    help='URL to short', 
    location='args')

resource_fields = api.model('Resource', {
    'result': fields.String,
})

@ns.route('/shorten')
class Acortar(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()

        return {
         "result": 'Su url acortada es: '+ acortador.acortar_url(args['url'])
        }, 200

@app.route("/<url_hash>")
def redirect_to(url_hash):
    return redirect(acortador.get_url(url_hash))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)