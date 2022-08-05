# Import Python Package
import jwt
import base64

payload = {"user": "Lanre", "role": "Admin"}
algo = 'HS256'  # HMAC-SHA 256
secret = 'learning'

# Encode a JWT
encoded_jwt = jwt.JWT().encode(payload, secret, alg=algo)
print(encoded_jwt)


# Decode a JWT
decoded_jwt = jwt.decode(encoded_jwt, secret, verify=True)
print(decoded_jwt)


# Decode with Simple Base64 Encoding
decoded_base64 = base64.b64decode(str(encoded_jwt).split(".")[1]+"==")
print(decoded_base64)
