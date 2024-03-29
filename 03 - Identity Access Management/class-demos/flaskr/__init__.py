import base64
import jwt
from flask import Flask


def create_app(test_config=None):

    app = Flask(__name__)

    # Import Python Package
    payload = {"user": "Lanre", "role": "Admin"}
    algo = 'HS256'  # HMAC-SHA 256
    secret = 'learning'

    # Encode a JWT
    encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
    print(encoded_jwt)

    # Decode a JWT
    decoded_jwt = jwt.decode(encoded_jwt, secret, verify=True)
    print(decoded_jwt)

    # Decode with Simple Base64 Encoding
    decoded_base64 = base64.b64decode(str(encoded_jwt).split(".")[1]+"==")
    print(decoded_base64)

    return app
