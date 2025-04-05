import secrets
import base64

# Generate a 32-byte random key
secret_key = base64.b64encode(secrets.token_bytes(32)).decode('utf-8')
print(f"Generated JWT Secret Key: {secret_key}") 