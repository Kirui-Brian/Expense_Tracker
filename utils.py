from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_access_token(identity):
    return jwt.create_access_token(identity=identity)

def jwt_required():
    return jwt.jwt.required()