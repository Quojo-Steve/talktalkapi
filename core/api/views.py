from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView 
from core.models import User, Profile
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, ProfileSerializer, UserSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token        # ...
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]

    return Response(routes)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
        if request.method == "GET":
            user = request.user
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            user = request.user
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def everyone(request):
    user = request.user
    people = Profile.objects.exclude(user=user)
    
    # Serialize both the Profile and User data
    profile_serializer = ProfileSerializer(people, many=True)
    user_serializer = UserSerializer(User.objects.filter(id__in=people.values('user_id')), many=True)  # Serialize User data
    
    # Combine the serialized data
    combined_data = []
    for profile_data, user_data in zip(profile_serializer.data, user_serializer.data):
        combined_data.append({**profile_data, 'user': user_data})
    
    return Response(combined_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def person(request, id):
    try:
        pers = Profile.objects.get(id=id)
        profile_serializer = ProfileSerializer(pers)
        
        # Get the corresponding User object
        user = pers.user
        user_serializer = UserSerializer(user)
        
        # Create a dictionary with both sets of data
        combined_data = {
            'profile': profile_serializer.data,
            'user': user_serializer.data
        }
        
        return Response(combined_data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)