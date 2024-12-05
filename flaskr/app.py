from flaskr import create_app
from .modelos import db
from flask_restful import Api
from .vistas import VistaSignIn, VistaLogIn
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = create_app('default')
app_context = app.app_context()
app_context.push()
CORS(app)
db.init_app(app)
db.create_all()

api = Api(app)

api.add_resource(VistaLogIn, '/login')  
api.add_resource(VistaSignIn, '/signin') 

jwt = JWTManager(app)
