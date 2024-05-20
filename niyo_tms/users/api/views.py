from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
# from niyo_tms.users.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer

User = get_user_model()

from .serializers import UserSerializer

from rest_framework import generics



class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    A viewset for retrieving, listing, updating, and accessing the authenticated user.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        """
        Get the queryset of users, filtering to only the authenticated user.

        This method ensures that only the authenticated user's data is returned.
        """
        assert isinstance(self.request.user.id, int)
        # Filter the queryset to only include the authenticated user
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        """
        Action to retrieve details of the authenticated user.

        This action returns details of the authenticated user.
        """
        # Serialize the authenticated user and return the data
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
class RegisterView(APIView):
    """
    A view for registering new users.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests to register a new user.

        This method validates the user registration data and saves the new user if valid.
        """
        # Serialize the user registration data
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new user if the data is valid
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        # Return errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
