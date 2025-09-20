from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer


@extend_schema(
    request=UserRegistrationSerializer,
    responses={201: UserSerializer}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_serializer = UserSerializer(user)
        return Response({
            'user': user_serializer.data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=UserLoginSerializer,
    responses={200: {
        'type': 'object',
        'properties': {
            'access_token': {'type': 'string'},
            'refresh_token': {'type': 'string'},
            'user': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'full_name': {'type': 'string'},
                    'is_super_user': {'type': 'boolean'},
                    'created_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        }
    }}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: UserSerializer}
)
@api_view(['GET'])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)