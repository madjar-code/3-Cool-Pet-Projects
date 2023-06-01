from enum import Enum
from django.db.models import QuerySet
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    CreateAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from users.models import User
from texts.models import TextBlock
from .serializers import (
    SimpleTextBlockSerializer,
    TextBlockSerializer,
    CUTextBlockSerializer,
)


class ErrorMessages(str, Enum):
    NO_USER = 'User with `username` no found'
    NO_TEXT_BLOCK = 'Text block with `hash` no found'


class TextBlockListView(ListAPIView):
    parser_classes = (JSONParser,)
    serializer_class = SimpleTextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.text_objects.all()

    @swagger_auto_schema(operation_id='all_text_blocks')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TextsForUser(ListAPIView):
    parser_classes = (JSONParser,)
    serializer_class = SimpleTextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.text_objects.all()

    @swagger_auto_schema(operation_id='text_blocks_for_user')
    def get(self, request: Request, username: str) -> Response:
        user: User = User.objects.filter(username=username).first()
        if not user:
            return Response({'error': ErrorMessages.NO_USER.value},
                            status=status.HTTP_404_NOT_FOUND)
        text_blocks: QuerySet[TextBlock] = self.queryset.filter(author=user)
        serializer = self.serializer_class(text_blocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTextBlockView(CreateAPIView):
    parser_classes = (JSONParser,)
    serializer_class = CUTextBlockSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_id='create_text_block')
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        current_user: User | AnonymousUser = request.user
        if isinstance(current_user, AnonymousUser):
            current_user = None
        serializer.save(author=current_user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateTextBlockView(UpdateAPIView):
    parser_classes = (JSONParser,)
    serializer_class = CUTextBlockSerializer
    queryset = TextBlock.objects.all()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_id='update_text_block')
    def put(self, request: Request, hash: str) -> Response:
        text_block: TextBlock = self.queryset.filter(hash=hash).first()
        if not text_block:
            return Response({'error': ErrorMessages.NO_TEXT_BLOCK.value},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            text_block, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TextBlockDetailsView(RetrieveAPIView):
    parser_classes = (JSONParser,)
    serializer_class = TextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.text_objects.all()
    lookup_field = 'hash'

    @swagger_auto_schema(operation_id='text_block_detail')
    def get(self, request: Request, hash: str) -> Response:
        text_block: TextBlock = self.queryset.filter(hash=hash).first()
        if not text_block:
            return Response({'error': ErrorMessages.NO_TEXT_BLOCK.value},
                            status=status.HTTP_404_NOT_FOUND)
        serializer: TextBlockSerializer = self.serializer_class(text_block)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
