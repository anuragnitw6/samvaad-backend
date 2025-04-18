from flask import Flask
# from Scripts.society import blp as SocietyBluePrint
from user import blp as UserBluePrint
from flask_smorest import Api 
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from marshmallow import ValidationError
app = Flask(__name__)
app = Flask(__name__, template_folder='template')
app.debug = True
app.config['DEBUG'] = True

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

@app.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {"error": e.messages}, 400

# api.register_blueprint(SocietyBluePrint)
api.register_blueprint(UserBluePrint)


