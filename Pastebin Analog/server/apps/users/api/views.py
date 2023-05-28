from rest_framework import status
from rest_framework.generics import\
    GenericAPIView
from rest_framework.parsers import\
    MultiPartParser, FormParser, JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import *


class RegisterAPIView(GenericAPIView):
    """Register user"""
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = RegisterSerializer
    
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    """Login user"""
    parser_classes = (JSONParser,)
    serializer_class = LoginSerializer
    
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_200_OK)
