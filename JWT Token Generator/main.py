import jwt  # PyJWT library for encoding and decoding JWTs
import datetime  # For setting token expiration time

# Secret key used for signing and verifying JWTs.
# IMPORTANT: In production, keep this secret and store it in environment variables.
SECRET_KEY = "your-very-secret-key-keep-it-safe!"

# Algorithm used to sign the JWT. "HS256" means HMAC with SHA-256.
ALGORITHM = "HS256"

def generate_token(expiration_minutes=1440):
    """
    Generate a JWT token with only an expiration claim.
    
    Args:
        expiration_minutes (int): How many minutes before the token expires (default 1440 = 24 hours).
    
    Returns:
        str: The encoded JWT string.
    """
    # Create the payload with expiration time (exp claim)
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    }
    # Encode (sign) the JWT using the secret key and algorithm
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token):
    """
    Verify and decode a JWT token.
    
    Args:
        token (str): The JWT string to verify.
    
    Returns:
        dict: The decoded payload if valid.
        None: If token is expired or invalid.
    """
    try:
        # Decode (verify) the JWT using the secret key and algorithm
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        # If the token's expiration time has passed
        print("Error: Token expired")
    except jwt.InvalidTokenError:
        # If the token signature or structure is invalid
        print("Error: Invalid token")
    return None

# Example usage of the functions
if __name__ == "__main__":
    # Generate a token that expires in 30 minutes
    token = generate_token(30)
    print("Generated JWT:", token)

    # Verify the token and decode the payload
    decoded = verify_token(token)
    if decoded:
        print("Decoded payload:", decoded)
