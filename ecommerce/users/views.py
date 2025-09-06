from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer
)
from .utils import get_token_key, redis_client, access_token_lifetime, RedisJWTAuthentication

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """View for user registration."""
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'User registered successfully',
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view that uses email instead of username."""
    
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data["refresh"]
        access_token = response.data["access"]
        
        refresh_token_key = get_token_key(refresh_token)
        redis_client.setex(refresh_token_key, 60*60*24*7, "valid")

        access_token_key = get_token_key(access_token)
        redis_client.setex(access_token_key,
                         int(access_token_lifetime.total_seconds()),
                         "valid")
        return response
    

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        token_key =get_token_key(refresh_token)
        
        if not redis_client.exists(token_key):
            raise InvalidToken("refresh token has been expired!")
        return super().post(request, *args, **kwargs)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating user profile."""
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """View for changing user password."""
    
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    authentication_classes = [RedisJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        access_token = request.headers.get("Authorization").split()[1]
        refresh_token = request.data.get("refresh")

        if access_token:
            redis_client.delete(get_token_key(access_token))
        
        if refresh_token:
            token_key = get_token_key(refresh_token)
            redis_client.delete(token_key)
        
        return Response({'message':'logged out successfully!'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([RedisJWTAuthentication])
def user_info(request):
    """Get current user information."""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)
