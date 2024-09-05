from rest_framework.decorators import api_view
from user_app.api.serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

@api_view(['POST',])
def LoginUser(request):
    username=request.data.get('username')
    password=request.data.get('password')
    user=authenticate(username=username,password=password)
    if user is not None:
        data={}
        data['response']='Successfully authenticated'
        refresh=RefreshToken.for_user(user)
        data['token']={
                        'refresh':str(refresh),
                        'access':str(refresh.access_token)
                        }
    else:
        data={}
        data['response']='Error'
    return Response(data)

@api_view(['POST',])
def RegisterUser(request):
    serializer=RegisterSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        acc=serializer.save()
        data['response']='Successfully registered a new user'
        data['username']=serializer.data['username']
        data['email']=acc.email
        refresh=RefreshToken.for_user(acc)
        data['token']={
                        'refresh':str(refresh),
                        'access':str(refresh.access_token)
                        }
    else:
        data = serializer.errors
    return Response(data,status=status.HTTP_201_CREATED)

@api_view(['POST',])
def LogoutView(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)