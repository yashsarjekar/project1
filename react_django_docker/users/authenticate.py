import jwt
from datetime import datetime, timedelta
from users.constants import AUTHENTICATION_SECRET_KEY
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from users.services.user_services.user_services import UserService

def generate_user_token(user):
    payload =  {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'iat': datetime.utcnow()
    }
    return jwt.encode(
        payload, 
        AUTHENTICATION_SECRET_KEY,
        algorithm='HS256'
    ).decode('utf-8')


class JWTAuthentication(BaseAuthentication):
    
    def __init__(self) -> None:
        self.__user_service = UserService()
        super().__init__()


    def authenticate(self, request):
        token = request.COOKIES.get('jwt')
        payload =  None
        if token:
            try:
                payload = jwt.decode(
                    token, 
                    AUTHENTICATION_SECRET_KEY, 
                    algorithms=['HS256']
                )
            except jwt.ExpiredSignatureError: 
                raise exceptions.AuthenticationFailed('unauthenticated')
        else:
            return None
        if payload:
            user =  self.__user_service.get_user_using_id(
                id=payload['user_id']
            )

            if user is None:
                raise exceptions.AuthenticationFailed('User not found!')
            else:
                return (user[0], None)