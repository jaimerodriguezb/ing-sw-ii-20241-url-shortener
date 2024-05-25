from flask import Flask
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from modelo.model import AcortadorUrl, redirection

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

acortador_url = AcortadorUrl()
redireccionador = redirection()

api = Api(
    app, 
    version='1.0', 
    title='URL Shortener and Redirector',
    description='API for shortening URLs with phishing detection and retrieving original URLs from shortened URLs'
)

# Namespace for URL Shortener
ns_shorten = api.namespace('url', description='URL Shortening Operations')

shorten_parser = api.parser()
shorten_parser.add_argument(
    'url', 
    type=str, 
    required=True, 
    help='URL to shorten', 
    location='args'
)

shorten_resource_fields = api.model('ShortenResource', {
    'result': fields.String,
})

@ns_shorten.route('/shorten')
class Acortar(Resource):

    @api.doc(parser=shorten_parser)
    @api.marshal_with(shorten_resource_fields)
    def get(self):
        args = shorten_parser.parse_args()
        return {
            "result": acortador_url.acortar_url(args['url'])
        }, 200

# Namespace for URL Redirector
ns_redirect = api.namespace('redirect', description='URL Redirection Operations')

redirect_parser = api.parser()
redirect_parser.add_argument(
    'url', 
    type=str, 
    required=True, 
    help='Shortened URL', 
    location='args'
)

redirect_resource_fields = api.model('RedirectResource', {
    'result': fields.String,
})

@ns_redirect.route('/shortened')
class Redireccionar(Resource):

    @api.doc(parser=redirect_parser)
    @api.marshal_with(redirect_resource_fields)
    def get(self):
        args = redirect_parser.parse_args()
        original_url = redireccionador.redireccionar_url(args['url'])
        if original_url:
            return {
                "result": original_url
            }, 200
        else:
            return {
                "result": "Error: URL not found in the database"
            }, 404

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
