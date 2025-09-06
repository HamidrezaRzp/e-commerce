from django.conf import settings
import hashlib
from datetime import timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import authentication

access_token_lifetime = getattr(settings, "SIMPLE_JWT", {}).get(
    "ACCESS_TOKEN_LIFETIME", timedelta(minutes=60))

redis_client = settings.REDIS_CLIENT

def get_token_key(token: str) -> str :
    return hashlib.sha256(token.encode()).hexdigest()

def is_token_valid_in_redis(token: str) -> bool:
    """Check if a token exists and is valid in Redis."""
    token_key = get_token_key(token)
    return redis_client.exists(token_key)

class RedisJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class that validates JWT tokens against Redis.
    This ensures that logged out tokens are invalid even if they haven't expired.
    """
    
    def authenticate(self, request):
        # Get the JWT authentication instance
        jwt_auth = JWTAuthentication()
        
        try:
            # First, try to authenticate with JWT
            user_auth_tuple = jwt_auth.authenticate(request)
            if user_auth_tuple is None:
                return None
                
            user, token = user_auth_tuple
            
            # Check if the token is valid in Redis
            if not is_token_valid_in_redis(str(token)):
                # Token has been invalidated (e.g., user logged out)
                raise InvalidToken("Token has been invalidated")
                
            return user_auth_tuple
            
        except InvalidToken:
            return None
        except Exception:
            return None
    
    def authenticate_header(self, request):
        return 'Bearer realm="api"'
