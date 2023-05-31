from enum import Enum
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
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
)


class ErrorMessages(str, Enum):
    NO_USER = 'User with `username` no found'
    NO_TEXT_BLOCK = 'Text block with `hash` no found'


class TextBlockListView(ListAPIView):
    parser_classes = (JSONParser,)
    serializer_class = SimpleTextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.active_objects.all()

    @swagger_auto_schema(operation_id='all_text_blocks')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TextsForUser(ListAPIView):
    parser_classes = (JSONParser,)
    serializer_class = SimpleTextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.active_objects.all()

    @swagger_auto_schema(operation_id='text_blocks_for_user')
    def get(self, request: Request, username: str) -> Response:
        """
        Get text blocks to user by username
        """
        user: User = User.objects.filter(username=username).first()
        if not user:
            return Response({'error': ErrorMessages.NO_USER.value},
                            status=status.HTTP_404_NOT_FOUND)
        text_blocks: QuerySet[TextBlock] = self.queryset.filter(author=user)
        serializer = self.serializer_class(text_blocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TextBlockDetailsView(RetrieveAPIView):
    parser_classes = (JSONParser,)
    serializer_class = TextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.active_objects.all()
    lookup_field = 'hash'

    @swagger_auto_schema(operation_id='text_block_detail')
    def get(self, request: Request, hash: str) -> Response:
        text_block: TextBlock = self.queryset.filter(hash=hash).first()
        if not text_block:
            return Response({'error': ErrorMessages.NO_TEXT_BLOCK.value},
                            status=status.HTTP_404_NOT_FOUND)
        serializer: TextBlockSerializer = self.serializer_class(text_block)
        return Response(data=serializer.data, status=status.HTTP_200_OK)