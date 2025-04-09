# from flask import Flask, app, render_template

# app = Flask(__name__, template_folder='template')

# @app.route('/home')
# def index():
#     return render_template('index.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/service')
# def service():
#     return render_template('service.html')

# @app.route('/team')
# def team():
#     return render_template('team.html')

# @app.route('/why')
# def why():
#     return render_template('why.html')
    
# @app.route('/login')
# def login():
#     return render_template('login.html')
from flask import Flask
# from Scripts.society import blp as SocietyBluePrint
from user import blp as UserBluePrint
from flask_smorest import Api 
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST

app = Flask(__name__)
app = Flask(__name__, template_folder='template')

app.config["PROPAGATE_EXCEPTIONS"] = True 
app.config["API_TITLE"] = "Samvaad Rest API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/samvaad-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config["JWT_SECRET_KEY"] = "154281130814958933425240769184967185190"

api = Api(app)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        {
            "description":"User has been logged out",
            "error": "token_revoked"
        },
        401
    )



# api.register_blueprint(SocietyBluePrint)
api.register_blueprint(UserBluePrint)


