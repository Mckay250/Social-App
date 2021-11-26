from django.http import response
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from ipware import get_client_ip


class SignUpView(APIView):
    def post(self, request):
        client_ip = get_client_ip(request)
        if client_ip is not None:
            request.data['ip_address'] = client_ip
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        
# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         # fetch user from the datastore
#         user = User.objects.filter(email=email).first()

#         # raise auth failed exception if user is not found
#         if user is None:
#             raise AuthenticationFailed('Invalid login credentials')
#         # raise auth failed exceprion if password is wrong
#         if not user.check_password(password):
#             raise AuthenticationFailed('Invalid login credentials')

#         # create jwt token
#         payload = {
#             'id' : user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=40),
#             'iat': datetime.datetime.utcnow()
#         }
#         token = encode_jwt(payload=payload)

#         # initialize response
#         response = Response({'message': 'Login Successful'})

#         # set token to response as cookie
#         response.set_cookie(key='jwt', value=token, httponly=True)

#         return response


class UserView(APIView):
    def get(self, request):

        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)

        return Response(serializer.data)

        
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# # returns a token created from a payload
# def encode_jwt(payload):
#     return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

# # returns the payload inside a token
# def decode_jwt(token):
#     return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])